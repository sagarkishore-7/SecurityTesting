from fuzzingbook.Grammars import is_valid_grammar

BFGRAMMAR = {
    "<start>": ["<bf_program>"],

    "<bf_program>": ["<bf_command>", "<bf_loop>", "<bf_program> <bf_program>"],

    "<bf_command>": ["+","-", ">", "<", ".", ","],

    "<bf_loop>": ["[ <bf_program> ]"]
}

assert is_valid_grammar(BFGRAMMAR)
