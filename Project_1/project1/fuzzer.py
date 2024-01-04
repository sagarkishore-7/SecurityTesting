from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer, opts
from grammar import DBManager, grammar
from fuzzingbook.Grammars import trim_grammar

# Instantiate the database for the SQL fuzzer
custom_db = DBManager()

class EnhancedGrammarFuzzer(ProbabilisticGeneratorGrammarFuzzer):

    def create_tree(self):
        # Override to generate a complete tree with applied constraints
        while True:
            syntax_tree = super().fuzz_tree()
            return syntax_tree

    def pick_expansion(self, node, children_to_expand):
        # Decide which child node to expand based on the grammar's order
        (nonterminal, children) = node
        assert isinstance(children, list)

        if len(children_to_expand) == 1:
            return super().choose_tree_expansion(node, children_to_expand)

        chosen_expansion = self.get_chosen_expansion(node)
        order_of_expansion = opts(chosen_expansion)
        if order_of_expansion is None:
            return super().choose_tree_expansion(node, children_to_expand)

        # Iterate to find the child with the lowest expansion order
        chosen_child = None
        for i, child in enumerate(children_to_expand):
            child_order = order_of_expansion(child)
            if chosen_child is None or child_order < order_of_expansion(chosen_child):
                chosen_child = i

        assert chosen_child is not None
        return chosen_child

class Fuzzer:
    def __init__(self):
        self.grammar_spec = grammar
        self.setup_fuzzer()

    def setup_fuzzer(self):
        self.execution_count = 0
        self.grammar_spec["<start>"] = [("<create_table>", opts(prob=1.0)),
                                        "<create_index_or_view>",
                                        "<additional_commands>",
                                        ]
        self.sql_fuzzer = EnhancedGrammarFuzzer(trim_grammar(self.grammar_spec))

    def fuzz_one_input(self) -> str:
        output = self.sql_fuzzer.fuzz()

        if 10 <= self.execution_count <= 20:
            self.grammar_spec["<start>"] = ["<create_table>",
                                            ("<create_index_or_view>", opts(prob=1.0)),
                                            "<additional_commands>",
                                            ]
            self.sql_fuzzer = EnhancedGrammarFuzzer(trim_grammar(self.grammar_spec))
        elif self.execution_count > 20:
            self.grammar_spec["<start>"] = ["<create_table>",
                                            "<create_index_or_view>",
                                            "<additional_commands>",
                                            ]
            self.sql_fuzzer = EnhancedGrammarFuzzer(trim_grammar(self.grammar_spec))

        self.execution_count += 1
        return output

# Usage
if __name__ == "__main__":
    fuzz_instance = Fuzzer()
    for _ in range(30):
        print(fuzz_instance.fuzz_one_input())
