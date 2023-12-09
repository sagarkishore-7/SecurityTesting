"""
Use this file to implement your solution for exercise 3-1 a.
"""
from trees import expr_tree_1, expr_tree_2

def find_subtrees(tree, symbol):
    subtrees = []

    # Check if the current node is a tuple and the first symbol matches the selected symbol
    if isinstance(tree, tuple) and tree[0] == symbol:
        # Add the subtree to the list
        subtrees.append(tree)
    # Recursively traverse the child node of the current node
    if tree[1]:
        for child in tree[1]:
            subtrees.extend(find_subtrees(child, symbol))

    return subtrees


tree1 = find_subtrees(expr_tree_1, '<integer>')
tree2 = find_subtrees(expr_tree_2, '<integer>')
print(tree1)
print(tree2)