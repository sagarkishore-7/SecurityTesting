from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
import grammar
import random

class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
    
    def setup_fuzzer(self):
        # This function may be changed.
        self.fuzzer = EvenFasterGrammarFuzzer(self.grammar)

    def fuzz_one_input(self) -> str:
        return self.generate_from_grammar(self.grammar, "<start>")

    def generate_from_grammar(self, grammar, key):
        if key not in grammar:
            return key
        expansion = random.choice(grammar[key])
        return ''.join(self.generate_from_grammar(grammar, token) for token in expansion)