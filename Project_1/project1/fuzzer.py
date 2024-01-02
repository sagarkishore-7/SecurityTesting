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
        self.used_rules = set()

    def fuzz_one_input(self) -> str:
        # Entry point for the fuzzing process.
        # Reset the used rules before each fuzzing to ensure independent generations.
        self.used_rules.clear()
        return self.generate_from_grammar("<start>", 0)

    def generate_from_grammar(self, key, depth):
        # Check for the termination condition based on depth.
        if depth > self.max_depth:
            # Attempt to finalize the generation with terminal symbols if possible.
            return self.finalize_with_terminal(key)

        # Choose a random production rule for the current key.
        production = random.choice(self.grammar[key])

        # If the production is a terminal symbol, return it directly.
        if self.is_terminal(production):
            return production

        # Recursively generate strings for each symbol in the chosen production rule.
        result = ''
        for symbol in production:
            if symbol in self.grammar:
                # Increase depth for non-terminal symbols.
                result += self.generate_from_grammar(symbol, depth + 1)
            else:
                result += symbol

        return result

    def finalize_with_terminal(self, key):
        # If maximum depth is reached, use terminal symbols if available.
        if key not in self.grammar:
            return key  # The key itself might be a terminal symbol.
        # Filter out non-terminal production rules.
        terminals = [rule for rule in self.grammar[key] if self.is_terminal(rule)]
        if terminals:
            # Choose a random terminal production rule.
            return random.choice(terminals)
        else:
            # As a last resort, use the first symbol of the first rule.
            return self.grammar[key][0][0]

    def is_terminal(self, symbols):
        # Check if all symbols in a production rule are terminal.
        return all(symbol not in self.grammar for symbol in symbols)

    @property
    def max_depth(self):
        return 10