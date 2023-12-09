"""
Use this file to implement your solution for exercise 3-2 a.
"""

RE_GRAMMAR_EXPANDED = {
    '<start>': ['<alternative>', '^<alternative>', '<alternative>$', '^<alternative>$'],
    '<alternative>': ['<concat>', '<concat>|<alternative>'],
    '<concat>': ['', '<concat><regex>'],
    '<regex>': ['<symbol>', '<symbol>*', '<symbol>+', '<symbol>?', '<symbol>{<range>}'],
    '<symbol>': ['.', '<char>', '(<alternative>)', '<char_0>', '(<alternative_0>)'],
    '<char>': ['a', 'b', 'c'],
    '<char_0>': ['a', 'b', 'c'],
    '<range>': ['<num>', ',<num>', '<range_0>', ',<range_0>'],
    '<num>': ['1', '2'],
    '<range_0>': ['<num_0>', ',<num_0>'],
    '<num_0>': ['1', '2'],
    '<alternative_0>': ['<concat_0>', '<concat_0>|<alternative_0>'],
    '<concat_0>': ['', '<concat_0><regex_0>'],
    '<regex_0>': ['<symbol_0>', '<symbol_0>*', '<symbol_0>+', '<symbol_0>?', '<symbol_0>{<range_0>}'],
    '<symbol_0>': ['.', '<char_0>', '(<alternative_0>)'],
}
