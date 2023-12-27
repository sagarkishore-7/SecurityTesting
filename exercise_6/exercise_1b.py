import re
from exercise_1a import *

def generalize(g: dict, cnt_inputs: int) -> dict:

    digits_and_letters = {
        '<digits>': ['<digit>', '<digit><digits>'],
        '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        '<letters>': ['<letter>', '<letter><letters>'],
        '<letter>': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                     'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    }

    for key, rules in g.items():
        distinct_rules = set(rules)

        if len(distinct_rules) < cnt_inputs / 2 or any('<' in rule for rule in rules):
            continue

        if all(re.match(r'^\d+$', rule) for rule in distinct_rules):
            g[key] = ['<digits>']
        elif all(re.match(r'^[a-zA-Z]+$', rule) for rule in distinct_rules):
            g[key] = ['<letters>']

    g.update(digits_and_letters)

    return g