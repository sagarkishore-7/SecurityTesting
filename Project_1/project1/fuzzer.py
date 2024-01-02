from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
import grammar
import random


class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()

    def setup_fuzzer(self):
        # This method can be used to set up any necessary pre-fuzzing configurations.
        self.max_depth = 10
        self.invocation_count = {}  # Track how many times we've called each rule.

    def fuzz_one_input(self) -> str:
        # Reset invocation count each time we generate a new fuzz input.
        self.invocation_count = {}
        return self.generate_from_grammar("<start>", 0)

    def generate_from_grammar(self, key, depth):
        if key not in self.grammar:
            return key
        elif depth > self.max_depth:
            return self.choose_terminal(key)
        else:
            self.invocation_count[key] = self.invocation_count.get(key, 0) + 1
            expansion = random.choice(self.grammar[key])
            return ''.join(
                self.generate_from_grammar(token, depth + 1 if token in self.grammar else depth) for token in expansion)

    def choose_terminal(self, key):
        # Choose a terminal production; if none are found, fall back to the simplest option.
        terminals = [prod for prod in self.grammar[key] if self.is_terminal(prod)]
        if terminals:
            return random.choice(terminals)
        else:
            # No terminal production is available; use the first token as a fallback.
            return self.grammar[key][0][0]

    def is_terminal(self, production):
        # Check if the production is terminal.
        return all(token not in self.grammar for token in production)