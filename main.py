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
        except TypeError:
            pass


    valid = False
    while not valid:
        storage = input('please enter your rough storage requirements (in terabytes): ')
        try:
            storage = int(storage)
            if storage > 0:
                valid = True
        except TypeError:
            pass

    valid = False
    while not valid:
        expertise = input('please enter your level of technical expertise (none / basic / moderate / high / expert): ').lower()
        if expertise == 'none' or expertise == 'basic' or expertise == 'moderate' or expertise == 'high' or expertise == 'expert':
            valid = True

    valid = False
    while not valid:
        security = input('please enter your security requirements between 1 and 10: ')
        if security == "":
            security = None
            valid = True
        else:
            try:
                security = int(security)
                if security >= 0 and security <= 10:
                    valid = True
            except TypeError:
                pass

    valid = False
    while not valid:
        sustainability = input('please enter your sustainability_requirements between 1 and 100: ')
        try:
            sustainability = float(sustainability)
            if sustainability >= 0 and sustainability <= 100:
                valid = True
        except TypeError:
            pass
    sustainability = sustainability / 100 # convert to percentage multiplier

    valid = False
    while not valid:
        top_priority = input('please enter your top priority (none / basic / moderate / high / expert): ').lower()

    valid = False
    while not valid:
        growth = input('please enter your growth multiplier expectation for the next five years: ')
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

    return {budget: budget, storage: storage, expertise: expertise, security: security, sustainability: sustainability, top_priority: top_priority, growth: growth}

