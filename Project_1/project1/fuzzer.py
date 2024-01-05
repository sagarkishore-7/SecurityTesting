from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer, opts, exp_order
from grammar import DBManager, grammar
from fuzzingbook.Grammars import trim_grammar

# Instantiate the database for the SQL fuzzer
custom_db = DBManager()


class EnhancedGrammarFuzzer(ProbabilisticGeneratorGrammarFuzzer):

    def fuzz_tree(self):
        while True:
            tree = GrammarFuzzer.fuzz_tree(self)
            return tree

    def choose_tree_expansion(self, tree, children_to_expand):
        """Choose a subtree from `children_to_expand` for expansion. Default behavior is random selection."""

        (symbol, tree_children) = tree
        assert isinstance(tree_children, list)

        if len(children_to_expand) == 1:
            return GrammarFuzzer.choose_tree_expansion(self, tree, children_to_expand)

        chosen_expansion = self.find_expansion(tree)
        specified_order = exp_order(chosen_expansion)
        if specified_order is None:
            return GrammarFuzzer.choose_tree_expansion(self, tree, children_to_expand)

        expandable_nonterminals = [c for c in tree_children if c[1] != []]
        assert len(expandable_nonterminals) == len(specified_order), "Order must have one element for each non-terminal"

        # Search for the expandable child with the lowest order
        lowest_order_index = None
        index = 0
        for i, child_to_expand in enumerate(children_to_expand):
            while index < len(expandable_nonterminals) and child_to_expand != expandable_nonterminals[index]:
                index += 1
            assert index < len(expandable_nonterminals), "Child to expand not found in non-terminals"
            if self.log:
                print(f"Expandable child #{i} {child_to_expand[0]} is ordered at {specified_order[index]}")

            if lowest_order_index is None or specified_order[index] < specified_order[lowest_order_index]:
                lowest_order_index = i

        assert lowest_order_index is not None

        if self.log:
            print(f"Selected expandable child #{lowest_order_index} {children_to_expand[lowest_order_index][0]}")
        return lowest_order_index


class Fuzzer:
    def __init__(self):
        self.grammar_spec = grammar
        self.setup_fuzzer()

    def setup_fuzzer(self):
        self.execution_count = 0
        self.grammar_spec["<start>"] = [("<ddl_statements-1>", opts(prob=1.0)),
                                        "<ddl_statements-2>",
                                        "<dml_statements>",
                                        ]
        self.sql_fuzzer = EnhancedGrammarFuzzer(trim_grammar(self.grammar_spec))

    def fuzz_one_input(self) -> str:
        output = self.sql_fuzzer.fuzz()

        if 5 <= self.execution_count <= 15:
            self.grammar_spec["<start>"] = ["<ddl_statements-1>",
                                            ("<ddl_statements-2>", opts(prob=1.0)),
                                            "<dml_statements>",
                                            ]
            self.sql_fuzzer = EnhancedGrammarFuzzer(trim_grammar(self.grammar_spec))
        elif self.execution_count > 15:
            self.grammar_spec["<start>"] = ["<ddl_statements-1>",
                                            "<ddl_statements-2>",
                                            "<dml_statements>",
                                            ]
            self.sql_fuzzer = EnhancedGrammarFuzzer(trim_grammar(self.grammar_spec))

        self.execution_count += 1
        return output


# Usage
if __name__ == "__main__":
    fuzz_instance = Fuzzer()
    for _ in range(30000):
        print(fuzz_instance.fuzz_one_input())
