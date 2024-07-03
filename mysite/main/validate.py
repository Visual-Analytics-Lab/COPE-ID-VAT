import re

def validate_variable_name(variable_name):
    # valid = True
    # invalid = False
    pattern = r'^[a-zA-Z@][a-zA-Z0-9@#\$,\._]*[a-zA-Z0-9@#\$,\.]?$'

    # List of reserved keywords
    reserved_keywords = {"ALL", "AND", "BY", "EQ", "GE", "GT", "LE", "LT", "NE", "NOT", "OR", "TO", "WITH",
                        "S1", "E1", "C1", "NET", "SUB", "TN", "CALC"}

    # Check if the length is within the allowed limit
    if len(variable_name) > 64:
        return False, "Variable name exceeds 64 characters."

    # Check if the last character is not a period or underscore
    elif variable_name[-1] in {'.', '_'}:
        return False, "The last character cannot be a period or underscore."

    # Check against the regex pattern
    elif not re.match(pattern, variable_name):
        return False, "Variable name contains invalid characters."

    # Check against reserved keywords
    elif variable_name.upper() in reserved_keywords:
        return False, "Variable name is a reserved keyword."

    # Check against special conditions for reserved key words (A, C, E, F, H, I, M, R, S or V followed by a number)
    elif re.match(r'^[ACEFHIMRSV][0-9]$', variable_name, re.IGNORECASE):
        return False, "Variable name cannot be a single letter followed by a number."

    else:
        return True, "None"