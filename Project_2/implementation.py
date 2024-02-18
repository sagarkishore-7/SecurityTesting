"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from fuzzingbook.Grammars import nonterminals
from helpers import *
from fuzzingbook.GrammarFuzzer import GrammarFuzzer


def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    """
    Instantiate the constraint pattern with nonterminals and return the set of instantiated constraints.
    """
    count = constraint_pattern.count("{}")
    possible_combinations = generate_possible_combinations(nonterminals, count)
    return {constraint_pattern.format(*combination) for combination in possible_combinations}


def generate_possible_combinations(nonterminals: list[str], count: int):
    stack = [((), count)]  # Initialize stack with empty tuple and count

    while stack:
        current_combination, remaining_count = stack.pop()

        if remaining_count == 0:
            yield current_combination
        else:
            for nonterminal in nonterminals:
                if is_nt(nonterminal):
                    stack.append((current_combination + (nonterminal,), remaining_count - 1))


def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:
    """
    Instantiate the abstract constraint with subtrees and return the set of instantiated constraints.
    """
    concrete_contraints_set = set()
    concrete_contraints_set = generate_concrete_contraints(concrete_contraints_set, abstract_constraint, nts_to_subtrees)
    return concrete_contraints_set

def generate_concrete_contraints(cc_set, abstract_constraint_string, nts_to_subtrees):
    stack = [(abstract_constraint_string, 0)]

    while stack:
        current_str, index = stack.pop()

        nt_index = current_str.find('<', index)
        if nt_index == -1:
            cc_set.add(current_str)
        else:
            nt_end_index = current_str.find('>', nt_index)
            nonterminal = current_str[nt_index:nt_end_index + 1]
            if nonterminal in nts_to_subtrees:
                for value in nts_to_subtrees[nonterminal]:
                    t2s = tree_to_string(value)
                    changed_str = current_str[:nt_index] + t2s + current_str[nt_end_index + 1:]
                    stack.append((changed_str, nt_index))

    return cc_set


def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    """
    Learn abstract constraints from the given constraint patterns and derivation trees.
    """
    common_nts = set(get_all_subtrees(derivation_trees[0]).keys())

    for tree in derivation_trees[1:]:
        common_nts &= set(get_all_subtrees(tree).keys())

    common_constraints = set()

    for pattern in constraint_patterns:
        instantiated_constraints = instantiate_with_nonterminals(pattern, common_nts)
        common_constraints.update(constraint for constraint in instantiated_constraints
                                  if all(check({constraint}, tree) for tree in derivation_trees))

    return common_constraints


def check(abstract_constraints: set[str], derivation_tree) -> bool:
    """
    Check if the derivation tree satisfies the given abstract constraints.
    """
    subtree_collection = get_all_subtrees(derivation_tree)
    result = True

    for abstract_constraint in abstract_constraints:
        for object in instantiate_with_subtrees(abstract_constraint, subtree_collection):
            try:
                result = eval(object)
            except:
                return False
            if not result:
                return result

    return result


def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:
    """
    Generate a valid sample string according to the given abstract constraints and grammar.
    """
    fuzzer = GrammarFuzzer(grammar)

    while True:
        input = fuzzer.fuzz()
        derivation_tree = next(EarleyParser(grammar).parse(input))
        satisfies_constraints = check(abstract_constraints, derivation_tree)

        if produce_valid_sample and satisfies_constraints:
            return input
        elif not produce_valid_sample and not satisfies_constraints:
            return input
