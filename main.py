def collect_inputs():
    """
    collect and validate inputs
    check actual docstring formatting
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
    check actual docstring formatting
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

