import sys
import os

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

import se2

MODULE = "se2"

def test_peep_1():
    do_test_peep(p=1, e=3, expected=True)

def test_peep_2():
    do_test_peep(p=3, e=1, expected=False)

def test_peep_3():
    do_test_peep(p=0, e=1, expected=False)

def test_peep_4():
    do_test_peep(p=1, e=0, expected=False)

def test_peep_5():
    do_test_peep(p=1, e=2, expected=False)

def test_peep_6():
    do_test_peep(p=2, e=3, expected=False)

def test_has_more_1():
    lst1 = []
    lst2 = []
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=False)

def test_has_more_2():
    lst1 = []
    lst2 = [1]
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=False)

def test_has_more_3():
    lst1 = [1]
    lst2 = [1]
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=False)

def test_has_more_4():
    lst1 = [1]
    lst2 = []
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=True)

def test_has_more_5():
    lst1 = [1, 2, 1]
    lst2 = [1, 2, 2]
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=True)

def test_has_more_6():
    lst1 = [1, 2, 2]
    lst2 = [2, 1, 1]
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=False)

def test_has_more_7():
    lst1 = [1, 2, 2, 1]
    lst2 = [2, 1, 1]
    do_test_has_more(lst1=lst1, lst2=lst2, target=1, expected=False)

def test_has_more_8():
    lst1 = [1, 1, 2, 2]
    lst2 = [2, 1, 1, 1, 1]
    do_test_has_more(lst1=lst1, lst2=lst2, target=2, expected=True)

def test_make_star_strings_1():
    lst = []
    do_test_make_star_strings(lst=lst, expected=[])

def test_make_star_strings_2():
    lst = [1]
    do_test_make_star_strings(lst=lst, expected=["*"])

def test_make_star_strings_3():
    lst = [3]
    do_test_make_star_strings(lst=lst, expected=["***"])

def test_make_star_strings_4():
    lst = [1, 2, 3]
    do_test_make_star_strings(lst=lst, expected=["*", "**", "***"])

def test_make_star_strings_5():
    lst = [1, 2, 3, 2, 0]
    do_test_make_star_strings(lst=lst, expected=["*", "**", "***", "**", ""])

def test_make_star_strings_6():
    lst = [2, 1, 5, 3, 3]
    do_test_make_star_strings(lst=lst, expected=["**", "*", "*****", "***", "***"])

def test_replace_1():
    do_test_replace(lst=[], replacee=1, replacer=2, expected=[])

def test_replace_2():
    do_test_replace(lst=[1], replacee=1, replacer=2, expected=[2])

def test_replace_3():
    do_test_replace(lst=[3], replacee=1, replacer=2, expected=[3])

def test_replace_4():
    do_test_replace(lst=[1, 2, 3, 4], replacee=1, replacer=2, expected=[2, 2, 3, 4])

def test_replace_5():
    do_test_replace(lst=[1, 2, 3, 4], replacee=4, replacer=3, expected=[1, 2, 3, 3])

def test_replace_6():
    do_test_replace(lst=[3, 2, 3, 2], replacee=2, replacer=1, expected=[3, 1, 3, 1])

def test_replace_7():
    do_test_replace(lst=[2, 2, 2, 2], replacee=2, replacer=1, expected=[1, 1, 1, 1])

def test_replace_8():
    do_test_replace(lst=[2, 2, 2, 2, 2], replacee=3, replacer=1, expected=[2, 2, 2, 2, 2])

def test_rows_and_columns_contain_1():
    grid = [[1, 2], [3, 1]]
    do_test_rows_and_columns_contain(grid=grid, target=1, expected=True)

def test_rows_and_columns_contain_2():
    grid = [[1, 2], [3, 1]]
    do_test_rows_and_columns_contain(grid=grid, target=2, expected=False)

def test_rows_and_columns_contain_3():
    grid = [[1, 2], [3, 2]]
    do_test_rows_and_columns_contain(grid=grid, target=2, expected=False)

def test_rows_and_columns_contain_4():
    grid = [[2, 1, 2], [1, 3, 1], [2, 2, 3]]
    do_test_rows_and_columns_contain(grid=grid, target=2, expected=False)

def test_rows_and_columns_contain_5():
    grid = [[3, 1, 2], [1, 3, 1], [2, 2, 3]]
    do_test_rows_and_columns_contain(grid=grid, target=3, expected=True)

def test_rows_and_columns_contain_6():
    grid = [[2, 1, 1], [3, 2, 3], [2, 1, 3]]
    do_test_rows_and_columns_contain(grid=grid, target=2, expected=False)

def test_rows_and_columns_contain_7():
    grid = [[2, 1, 1], [1, 2, 3], [2, 1, 3]]
    do_test_rows_and_columns_contain(grid=grid, target=1, expected=True)

grid0 = [[2, 1, 1, 2],
         [1, 2, 3, 1],
         [3, 3, 1, 2],
         [1, 2, 1, 3]]

def test_rows_and_columns_contain_8():
    do_test_rows_and_columns_contain(grid=grid0, target=1, expected=True)

def test_rows_and_columns_contain_9():
    do_test_rows_and_columns_contain(grid=grid0, target=2, expected=False)

def test_rows_and_columns_contain_10():
    do_test_rows_and_columns_contain(grid=grid0, target=3, expected=False)

def test_rows_and_columns_contain_1():
    grid = [[1, 2], [3, 1], [1, 3]]
    do_test_rows_and_columns_contain(grid=grid, target=1, expected=True)

def test_rows_and_columns_contain_2():
    grid = [[1, 2], [3, 1], [1, 3]]
    do_test_rows_and_columns_contain(grid=grid, target=3, expected=False)

# # #
#
# HELPER FUNCTIONS
#
# # #

def gen_recreate_msg(module, function, *params):
    params_str = ", ".join([str(p) for p in params])

    recreate_msg = "To recreate this test in ipython3 run:\n"
    recreate_msg += "  {}.{}({})".format(module, function, params_str)

    return recreate_msg


def check_none(actual, recreate_msg=None):
    msg = "The function returned None."
    msg += " Did you forget to replace the placeholder value we provide?"
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is not None, msg

def check_expected_none(actual, recreate_msg=None):
    msg = "The function is expected to return None."
    msg += " Your function returns: {}".format(actual)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual is None, msg


def check_type(actual, expected, recreate_msg=None):
    actual_type = type(actual)
    expected_type = type(expected)

    msg = "The function returned a value of the wrong type.\n"
    msg += "  Expected return type: {}.\n".format(expected_type.__name__)
    msg += "  Actual return type: {}.".format(actual_type.__name__)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert isinstance(actual, expected_type), msg


def check_equals(actual, expected, recreate_msg=None):
    msg = "Actual ({}) and expected ({}) values do not match.".format(actual, expected)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual == expected, msg


def check_list_unmodified(param_name, before, after, recreate_msg=None):
    msg = "You modified the contents of {} (this is not allowed).\n".format(param_name)
    msg += "  Value before your code: {}\n".format(before)
    msg += "  Value after your code:  {}".format(after)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert before == after, msg


# # #
#
# TEST HELPERS
#
# # #


def do_test_peep(p, e, expected):
    recreate_msg = gen_recreate_msg(MODULE, "peep", *(p, e))

    actual = se2.peep(p, e)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_has_more(lst1, lst2, target, expected):
    recreate_msg = gen_recreate_msg(MODULE, "has_more", *(lst1, lst2, target))

    actual = se2.has_more(lst1, lst2, target)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_make_star_strings(lst, expected):
    recreate_msg = gen_recreate_msg(MODULE, "make_star_strings", *(lst,))

    actual = se2.make_star_strings(lst)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_replace(lst, replacee, replacer, expected):
    recreate_msg = gen_recreate_msg(MODULE, "replace", *(lst, replacee, replacer))

    lst_copy = lst[:]
    actual = se2.replace(lst_copy, replacee, replacer)

    check_expected_none(actual, recreate_msg)
    check_equals(lst_copy, expected, recreate_msg)
    

def do_test_rows_and_columns_contain(grid, target, expected):
    recreate_msg = "  grid = {}\n".format(grid)
    recreate_msg += gen_recreate_msg(MODULE, "rows_and_columns_contain", *("grid", target))

    actual = se2.rows_and_columns_contain(grid, target)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)
    
