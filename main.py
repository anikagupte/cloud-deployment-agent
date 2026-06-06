"""
This is an AI agent that takes in a user's cloud computing requirements
and returns the best deployment solution for their business.
"""

import openpyxl
import google.generativeai as genai
genai.configure(api_key="")

def collect_inputs():
    """
    collect and validate inputs
    """

    valid = False
    while not valid:
        budget = input('please enter your monthly budget (in USD): ')
        try:
            budget = float(budget)
            if budget > 0:
                valid = True
        except ValueError:
            pass


    valid = False
    while not valid:
        storage = input('please enter your rough storage requirements (in terabytes): ')
        try:
            storage = int(storage)
            if storage > 0:
                valid = True
        except ValueError:
            pass

    valid = False
    while not valid:
        expertise = input('please enter your level of technical expertise (none / basic / moderate / high / expert): ').lower()
        if expertise == 'none' or expertise == 'basic' or expertise == 'moderate' or expertise == 'high' or expertise == 'expert':
            valid = True

    valid = False
    while not valid:
        security = input('please enter your security requirements between 1 and 10, or hit ENTER to skip: ')
        if security == "":
            security = None
            valid = True
        else:
            try:
                security = int(security)
                if security >= 0 and security <= 10:
                    security = security / 10 # normalise score
                    valid = True
            except ValueError:
                pass

    valid = False
    while not valid:
        sustainability = input('please enter your sustainability_requirements between 1 and 100: ')
        try:
            sustainability = float(sustainability)
            if sustainability >= 0 and sustainability <= 100:
                sustainability = sustainability / 100 # convert to percentage multiplier
                valid = True
        except ValueError:
            pass

    valid = False
    while not valid:
        growth = input('please enter your growth multiplier expectation for the next five years, or hit ENTER to skip: ')
        if growth == "":
            growth = None
            valid = True
        else:
            try:
                growth = int(growth)
                if growth > 0:
                    valid = True
            except TypeError:
                pass

    valid = False
    while not valid:
        top_priority = input('please enter your top priority (cost / security / sustainability / scalability): ').lower()
        if top_priority == 'cost' or top_priority == 'security' or top_priority == 'sustainability' or top_priority == 'scalability':
            valid = True

    return {"budget": budget, "storage": storage, "expertise": expertise, "security": security, "sustainability": sustainability, "top_priority": top_priority, "growth": growth}


def calculate_scores(inputs):
    """
    calculate scores using weightings
    :param inputs: dictionary of strings
    """

    cost_score = 1.0
    scalability_score = 1.0
    sustainability_score = 1.0
    geographic_coverage = 1.0
    security_score = 1.0
    complexity_score = 1.0
    customisability_score = 1.0
    management_overhead = 1.0

    if inputs["top_priority"] == "cost":
        cost_score *= 2
    elif inputs["top_priority"] == "security":
        security_score *= 2
    elif inputs["top_priority"] == "sustainability":
        sustainability_score *= 2
    elif inputs["top_priority"] == "scalability":
        scalability_score *= 2
        
    sustainability_score *= inputs["sustainability"]

    if inputs["security"] is not None:
        security_score *= inputs["security"]

    if inputs["expertise"] is not None:
        if inputs["expertise"] == "none":
            management_overhead *= 2
            complexity_score *= 2
        elif inputs["expertise"] == "basic":
            management_overhead *= 1.75
            customisability_score *= 1.25
            complexity_score *= 1.75
        elif inputs["expertise"] == "moderate":
            management_overhead *= 1.5
            customisability_score *= 1.5
            complexity_score *= 1.5
        elif inputs["expertise"] == "high":
            management_overhead *= 1.25
            customisability_score *= 1.75
            complexity_score *= 1.25
        else:
            customisability_score *= 2

    return {"Cost": cost_score, "Scalability": scalability_score, "Sustainability": sustainability_score, "Geographic Coverage": geographic_coverage, "Security": security_score, "Technical Complexity": complexity_score, "Customisability": customisability_score, "Management Overhead": management_overhead}


def load_scores(path):
    """
    load the data from excel spreadsheet (decision matrix)
    :param path: string
    """

    file = openpyxl.load_workbook(path)
    scores = {}

    for sheet_name in ["Provider_Scores", "Deployment_Scores", "Service_Scores"]:
            sheet = file[sheet_name]
            
            rows = [row for row in sheet.iter_rows(values_only=True) if any(cell is not None for cell in row)]
            
            first_row = rows[0]
            data_rows = rows[1:]
            
            headers = first_row[1:]
            criteria = [row[0] for row in data_rows]
            values = [row[1:] for row in data_rows]
            
            scores[sheet_name] = {
                "headers": headers,
                "criteria": criteria,
                "values": values
            }
        
    return scores
    

def score_sheet(data, weights):
    """
    multiply scores by their calculated weights
    :param data: dictionary of integers
    :param weights: dictionary fo floats
    """

    results = {}

    for header in data["headers"]:
        results[header] = 0

    for criterion_index, criterion in enumerate(data["criteria"]):
        for option_index, option in enumerate(data["headers"]):
            results[option] += data["values"][criterion_index][option_index] * weights[criterion]

    return results


def get_winner(results):
    """
    return provider with the highest score
    :param results: dictionary of floats
    """

    return max(results, key=results.get)


def get_recommendation(winners, inputs):
    """
    create prompt and call Gemini API
    :param winners: dictionary of strings
    :param inputs: dictionary of strings
    """

    prompt = "You are an experienced, specialised cloud deployment advisor for startups."
    prompt += f" Give them a detailed explanation of why the chosen stategy is best suited for them and produce a step by step plan for deployment."
    prompt += f" The plan should be extremely detailed, and also include further tips for management of the cloud infrastructure."
    prompt += f" Reference their specific inputs including priorities and constraints."
    prompt += f" Specifically reference sustainability from water and energy usage - the aim should be to save these resources."
    prompt += f" Consider techniques such as virtualisation and simply switching off power at night."
    prompt += f" Give advice on how to consistently maintain a reduction in energy/water usage."

    prompt += f" Monthly budget: {inputs['budget']} USD."
    prompt += f" Storage requirements: {inputs['storage']} TB."
    prompt += f" Technical expertise: {inputs['expertise']}."
    if inputs['security'] is not None:
        prompt += f" Security requirements (between 0 and 1): {inputs['security']}."
    prompt += f" Sustainability requirements (between 0 and 1): {inputs['sustainability']}."
    if inputs['growth'] is not None:
        prompt += f" Growth multiplier expectation for the next five years: {inputs['growth']}."
    prompt += f" Their top priority is {inputs['top_priority']}."
    
    prompt += f" Scores and weights have been calculated and the winners as follows. Use this to structure the advice."
    prompt += f" Provider: {winners['Provider']}."
    prompt += f" Provider: {winners['Deployment']}."
    prompt += f" Provider: {winners['Service']}."

    gemini_call = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
    return gemini_call.text