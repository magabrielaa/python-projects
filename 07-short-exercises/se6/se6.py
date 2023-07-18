"""
Short Exercises #6
"""


from tree import Tree


# Exercise 1
def sum_cubes(n):
    """
    Recursively calculates the sum of the first n positive cubes.

    Input:
        n: positive integer.

    Returns: (integer) the value of the sum 1^3 + 2^3 + ... + n^3.

    This function may not use any loops or list comprehensions.
    """
    if n == 1:
        # Base case
        return n
    elif n > 1:
        # Recursive case
        x = sum_cubes(n - 1)
        return x + n ** 3
        

# Exercise 2
def sublists(lst):
    """
    Computes all sublists of the input list.

    Input:
        lst: list of values

    Returns: (list of list of values) list of all sublists of lst.
    """
    if len(lst) == 0:
        return [[]]
    else:
        sublsts_minus_x = sublists(lst[1:])
        return sublsts_minus_x + [[lst[0]] + val for val in sublsts_minus_x]
    

# Exercise 3
def min_depth_leaf(tree):
    """
    Computes the minimum depth of a leaf in the tree (length of shortest
    path from the root to a leaf).

    Input:
        tree: a Tree instance.

    Returns: (integer) the minimum depth of of a leaf in the tree.
    """

    if tree.num_children() == 0:
        # Base case: the leaf is the node
        return 0
    else:
        # Recursive case:
        st_depths = [min_depth_leaf(st) for st in tree.children]
        return min(st_depths) + 1


# Exercise 4
def prune_tree(tree, keys_to_prune):
    '''
    Returns a new tree that is identical to the original tree, except
    that any node whose key is in keys_to_prune is removed, along with its
    descendants. If the key of the root is in keys_to_prune, then
    the function returns a null tree.

    Inputs:
        tree: a Tree instance.
        keys_to_prune: set of keys.

    Returns: (Tree) the pruned tree.
    '''

    if tree.key in keys_to_prune:
        return Tree(None)
    elif tree.num_children() == 0:
        return tree
    else:
        # Recursive case
        pruned = Tree(tree.key, tree.value)
        pruned_st = [prune_tree(st, keys_to_prune) for st in tree.children]
        
        for t in pruned_st:
            if t.key is not None:
                pruned.add_child(t)
        return pruned