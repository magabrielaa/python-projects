import sys
import os
import pytest

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

import se6
import util
from tree import Tree

MODULE = "se6"

# # #
#
# HELPER FUNCTIONS
#
# # #

def check_none(actual, recreate_msg=None):
    msg = "The method returned None."
    msg += " Did you forget a return statement?"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is not None, msg

def check_expected_none(actual, recreate_msg=None):
    msg = "The method is expected to return None."
    msg += " Your method returns: {}".format(actual)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is None, msg

def check_type(actual, expected, recreate_msg=None):
    actual_type = type(actual)
    expected_type = type(expected)

    msg = "The method returned a value of the wrong type.\n"
    msg += "  Expected return type: {}.\n".format(expected_type.__name__)
    msg += "  Actual return type: {}.".format(actual_type.__name__)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert isinstance(actual, expected_type), msg

def check_attribute(actual, attribute_name, recreate_msg=None):
    msg = "Your class should have a '{}' attribute.".format(attribute_name)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert hasattr(actual, attribute_name), msg

def check_attribute_type(actual, expected, recreate_msg=None):
    actual_type = type(actual)
    expected_type = type(expected)

    msg = "Your class has an attribute of the wrong type.\n"
    msg += "  Expected type: {}.\n".format(expected_type.__name__)
    msg += "  Actual type: {}.".format(actual_type.__name__)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert isinstance(actual, expected_type), msg

def check_equals(actual, expected, recreate_msg=None):
    msg = ("Actual ({}) and expected ({}) values " 
        "do not match.").format(actual, expected)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual == expected, msg

def check_parameter_unmodified(actual, expected, param, recreate_msg=None):
    msg = ("Parameter {} has been modified:\n"
        "Actual ({}) and original ({}) values of {}" 
        "do not match.").format(param, param, actual, expected)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual == expected, msg

def pretty_print_repr(x):
    return repr(x)

def gen_recreate_msg(module, function, *params, **kwparams):
    params_str = ", ".join([pretty_print_repr(p) for p in params])
    if len(kwparams) > 0:
        params_str += ", ".join(["{} = {}".format(k, repr(v)) 
            for k, v in kwparams.items()])
    lines = ["{}.{}({})".format(module, function, params_str)]
    return gen_recreate_msg_by_lines(lines)

def gen_recreate_msg_with_trees(module, function, tree_name, *params):
    params_str = "".join([", " + pretty_print_repr(p) for p in params])
    lines = ['import util',
             'trees = util.load_trees("sample_trees.json")',
             '{}.{}(trees["{}"]{})'.format(
                 module, function, tree_name, params_str)]
    return gen_recreate_msg_by_lines(lines)

def gen_recreate_msg_by_lines(lines):
    recreate_msg = "To recreate this test in ipython3 run:\n"
    recreate_msg += "  " + "\n  ".join(lines)
    return recreate_msg

def check_tree_equals(t, expected_t, recreate_msg):
    check_tree_helper(t, expected_t, 
        "Actual and expected values do not match:", recreate_msg)

def check_tree_unmodified(t, expected_t, recreate_msg):
    check_tree_helper(t, expected_t, "Tree has been modified:", recreate_msg)

def check_tree_helper(t, expected_t, top_msg, recreate_msg):
    expected_attributes = vars(expected_t)

    node_error_prefix = "Checking a node with " + ", ".join(
        ["{}={}".format(attr, repr(getattr(t, attr, "[not assigned]")))
        for attr in expected_attributes if attr != 'children']) + \
        "\n{}\n".format(top_msg)

    for attr in expected_attributes:
        assert hasattr(t, attr), \
            node_error_prefix + \
            "Node is missing attribute {}.\n".format(attr) + \
            recreate_msg

        if attr != 'children':
            assert getattr(t, attr) == getattr(expected_t, attr), \
            node_error_prefix + ("Node has incorrect {}. "
                "Got {}, expected {}.\n").format(attr,
                repr(getattr(t, attr)), repr(getattr(expected_t, attr))) + \
                recreate_msg
    
    expected_attributes_set = set(expected_attributes.keys())
    actual_attributes_set = set(vars(t).keys())
    assert actual_attributes_set == expected_attributes_set, \
            node_error_prefix + \
            "Node has extra attributes {}.\n".format(
                ", ".join(actual_attributes_set - expected_attributes_set)) + \
            recreate_msg


    children = list(t.children)
    expected_children = list(expected_t.children)

    if expected_children == []:
        assert children == [], node_error_prefix + \
            "Expected node to have no children, but it has children.\n" + \
            recreate_msg
    else:
        for c in children:
            assert isinstance(c, Tree), node_error_prefix + \
                "Node has a child that is not a Tree: {}\n".format(c) + \
                recreate_msg

        # This assumes no node has two children with the same key
        sorted_children = sorted(children, key=lambda st: st.key)
        sorted_expected_children = sorted(
            expected_children, key=lambda st: st.key)
        keys = [c.key for c in sorted_children]
        expected_keys = [c.key for c in sorted_expected_children]


        assert keys == expected_keys, node_error_prefix + \
            "Expected node to have children with keys {} " \
            "but the children's keys are {}.\n".format(expected_keys, keys) + \
            recreate_msg

        for child, expected_child in zip(sorted_children,
                                         sorted_expected_children):
            check_tree_helper(child, expected_child, top_msg, recreate_msg)

# # #
#
# TEST HELPERS
#
# # #

def do_test_sum_cubes(n):
    recreate_msg = gen_recreate_msg(MODULE, 'sum_cubes', n)
    actual = se6.sum_cubes(n)
    expected = sum(n ** 3 for n in range(n + 1))
    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)

def do_test_sublists(lst):
    original_lst = list(lst)
    recreate_msg = gen_recreate_msg(MODULE, 'sublists', original_lst)
    expected = [[x for j, x in enumerate(lst) if i ^ (2 ** j) < i] 
        for i in range(2 ** len(lst))]
    actual = se6.sublists(lst)
    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    for el in actual:
        check_type(el, [], recreate_msg)
    check_equals(sorted(actual), sorted(expected), recreate_msg)
    check_parameter_unmodified(lst, original_lst, "lst", recreate_msg)

def do_test_min_depth_leaf(trees_and_original_trees, tree_name, expected):
    trees, original_trees = trees_and_original_trees
    recreate_msg = gen_recreate_msg_with_trees(
        MODULE, 'min_depth_leaf', tree_name)
    actual = se6.min_depth_leaf(trees[tree_name])
    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)
    check_tree_unmodified(trees[tree_name], original_trees[tree_name], 
                          recreate_msg)

def do_test_prune_tree(trees_original_expected, tree_name, keys_to_prune):
    trees, original_trees, expected_trees = trees_original_expected
    recreate_msg = gen_recreate_msg_with_trees(
        MODULE, 'prune_tree', tree_name, keys_to_prune)
    actual = se6.prune_tree(trees[tree_name], keys_to_prune)
    check_none(actual, recreate_msg)
    check_type(actual, expected_trees[tree_name], recreate_msg)
    check_tree_equals(actual, expected_trees[tree_name], recreate_msg)
    check_tree_unmodified(trees[tree_name], original_trees[tree_name], 
                          recreate_msg)

# # #
#
# TESTS
#
# # #

def test_sum_cubes_1():
    do_test_sum_cubes(1)

def test_sum_cubes_2():
    do_test_sum_cubes(2)

def test_sum_cubes_3():
    do_test_sum_cubes(3)

def test_sum_cubes_4():
    do_test_sum_cubes(4)

def test_sum_cubes_5():
    do_test_sum_cubes(5)

def test_sum_cubes_6():
    do_test_sum_cubes(6)

def test_sum_cubes_7():
    do_test_sum_cubes(7)

def test_sum_cubes_8():
    do_test_sum_cubes(8)

def test_sum_cubes_9():
    do_test_sum_cubes(9)

def test_sum_cubes_10():
    do_test_sum_cubes(10)

def test_sum_cubes_11():
    do_test_sum_cubes(15)

def test_sum_cubes_12():
    do_test_sum_cubes(19)

def test_sum_cubes_13():
    do_test_sum_cubes(24)

def test_sum_cubes_14():
    do_test_sum_cubes(30)

def test_sum_cubes_15():
    do_test_sum_cubes(31)

def test_sum_cubes_16():
    do_test_sum_cubes(36)

def test_sum_cubes_17():
    do_test_sum_cubes(42)

def test_sum_cubes_18():
    do_test_sum_cubes(50)

def test_sum_cubes_19():
    do_test_sum_cubes(81)

def test_sum_cubes_20():
    do_test_sum_cubes(100)

def test_sublists_1():
    do_test_sublists(['apple'])

def test_sublists_2():
    do_test_sublists([12])

def test_sublists_3():
    do_test_sublists([True])

def test_sublists_4():
    do_test_sublists(['A', 'B'])

def test_sublists_5():
    do_test_sublists(["apple", "tomato"])

def test_sublists_6():
    do_test_sublists(['A', 'B', 'C'])

def test_sublists_7():
    do_test_sublists([50, 150, 100])

def test_sublists_8():
    do_test_sublists(['A', 'B', 'C', 'D'])

def test_sublists_9():
    do_test_sublists([50, 0, -1, 10])

def test_sublists_10():
    do_test_sublists([50, 0, -1, 10, 5])

def test_sublists_11():
    do_test_sublists(['A', 'B', 'C', 'D', 'E'])

def test_sublists_12():
    do_test_sublists(['U', 'V', 'W', 'X', 'Y', 'Z'])

def test_sublists_13():
    do_test_sublists(['water', 'apple', 'tomato', 'zucchini', 'corn', 'stew'])

def test_sublists_14():
    do_test_sublists(list(range(0, 70, 10)))

def test_sublists_15():
    do_test_sublists(list(range(70, 0, -10)))

def test_sublists_16():
    do_test_sublists(list('estuary'))

def test_sublists_17():
    do_test_sublists([1, 2, 3, 5, 8, 13, 21])

def test_sublists_18():
    do_test_sublists([1, -2, 3, -5, 8, -13, 21])

def test_sublists_19():
    do_test_sublists([8, 6, 7, 5, 3, 0, 9])

def test_sublists_20():
    do_test_sublists([1, 2, 3, 5, 8, 13, 21, 34])

def test_min_depth_leaf_1(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_1", 1)

def test_min_depth_leaf_2(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_2", 1)

def test_min_depth_leaf_3(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_3", 5)

def test_min_depth_leaf_4(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_4", 4)

def test_min_depth_leaf_5(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_5", 3)

def test_min_depth_leaf_6(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_6", 2)

def test_min_depth_leaf_7(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_7", 2)

def test_min_depth_leaf_8(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_8", 2)

def test_min_depth_leaf_9(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_9", 49)

def test_min_depth_leaf_10(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_10", 2)

def test_min_depth_leaf_11(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_11", 6)

def test_min_depth_leaf_12(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_12", 2)

def test_min_depth_leaf_13(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_13", 4)

def test_min_depth_leaf_14(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_14", 4)

def test_min_depth_leaf_15(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_15", 3)

def test_min_depth_leaf_16(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_16", 4)

def test_min_depth_leaf_17(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_17", 2)

def test_min_depth_leaf_18(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_18", 6)

def test_min_depth_leaf_19(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_19", 3)

def test_min_depth_leaf_20(trees_min_depth_leaf):
    do_test_min_depth_leaf(trees_min_depth_leaf, "tree_20", 2)

def test_prune_tree_1(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_1", {'D', 'B'})

def test_prune_tree_2(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_2", {'C', 'E'})

def test_prune_tree_3(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_3", {'E'})

def test_prune_tree_4(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_4", {'b', 'I', 'J', 'c', 'M'})

def test_prune_tree_5(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_5", {'Q', 'G', 'C'})

def test_prune_tree_6(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_6", {'V2'})

def test_prune_tree_7(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_7", {'V9'})

def test_prune_tree_8(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_8", set())

def test_prune_tree_9(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_9", {'V9', 'V8'})

def test_prune_tree_10(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_10", 
        {'V11', 'V8', 'V7', 'V4', 'V5'})

def test_prune_tree_11(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_11", {'V80', 'V90'})

def test_prune_tree_12(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_12", 
        {'V26', 'V9', 'V1', 'V6', 'V27'})

def test_prune_tree_13(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_13", {'V0', 'V1', 'V4', 'V3'})

def test_prune_tree_14(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_14", 
        {'V2', 'V0', 'V1', 'V7', 'V4', 'V6', 'V3', 'V5'})

def test_prune_tree_15(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_15", 
        {'V2', 'V48', 'V49', 'V46', 'V45', 'V47'})

def test_prune_tree_16(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_16", {'V10', 'V20', 'V30'})

def test_prune_tree_17(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_17", {'V3', 'V7'})

def test_prune_tree_18(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_18", 
        {'V26', 'V27', 'V24', 'V21', 'V28', 'V25', 'V23', 'V22'})

def test_prune_tree_19(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_19", {'V18'})

def test_prune_tree_20(trees_prune_tree):
    do_test_prune_tree(trees_prune_tree, "tree_20", 
        {'V12', 'V42', 'V46', 'V7', 'V30', 'V29', 'V60', 'V17', 'V36'})

# # #
#
# TEST TREES
#
# # #


@pytest.fixture(scope="session")
def trees_min_depth_leaf():
    """
    Fixture for loading the trees for min_depth_leaf
    """
    return get_trees()

@pytest.fixture(scope="session")
def trees_prune_tree():
    """
    Fixture for loading the trees for prune_tree
    """
    trees, original_trees = get_trees()
    expected_trees = util.load_trees("sample_trees_pruned.json")
    return trees, original_trees, expected_trees

def get_trees():
    trees = util.load_trees("sample_trees.json")
    original_trees = util.load_trees("sample_trees.json")
    return trees, original_trees