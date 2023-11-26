"""
Use this file to implement your solution for exercise 3-1 b.
"""
from exercise_1a import find_subtrees
from trees import expr_tree_1, expr_tree_2
import random


def replace_random_subtree(tree, symbol, subtrees):
    def replace_subtree(tree, old_subtree, new_subtree):
        if tree == old_subtree:
            return new_subtree
        else:
            new_children = [replace_subtree(child, old_subtree, new_subtree) for child in tree[1]]
            return tree[0], new_children

    possible_subtrees = find_subtrees(tree, symbol)

    if possible_subtrees:
        index_to_replace = random.randint(0, len(possible_subtrees) - 1)
        replacement_subtree = random.choice(subtrees)
        modified_tree = replace_subtree(tree, possible_subtrees[index_to_replace], replacement_subtree)
        return modified_tree
    else:
        return tree


symbol = '<digit>'
possible_subtrees = [('<digit>', [('1', None)]), ('<digit>', [('2', None)])]

modified_tree2 = replace_random_subtree(expr_tree_2, symbol, possible_subtrees)
modified_tree1 = replace_random_subtree(expr_tree_1, symbol, possible_subtrees)
print(modified_tree1)
print(modified_tree2)
