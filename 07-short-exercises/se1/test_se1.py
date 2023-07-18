import sys
import os

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

import se1

MODULE = "se1"

def test_add_one_and_multiply_1():
    do_test_add_one_and_multiply(a=0, x=0, expected=0)


def test_add_one_and_multiply_2():
    do_test_add_one_and_multiply(a=5, x=2, expected=12)


def test_add_one_and_multiply_3():
    do_test_add_one_and_multiply(a=5, x=0, expected=0)


def test_add_one_and_multiply_4():
    do_test_add_one_and_multiply(a=9, x=1, expected=10)


def test_add_one_and_multiply_5():
    do_test_add_one_and_multiply(a=9, x=-2, expected=-20)


def test_add_one_and_multiply_6():
    do_test_add_one_and_multiply(a=-11, x=2, expected=-20)


def test_out_of_range_1():
    do_test_out_of_range(x=5, lb=3, ub=10, expected=False)


def test_out_of_range_2():
    do_test_out_of_range(x=15, lb=3, ub=10, expected=True)


def test_out_of_range_3():
    do_test_out_of_range(x=3, lb=3, ub=10, expected=False)


def test_out_of_range_4():
    do_test_out_of_range(x=10, lb=3, ub=10, expected=False)


def test_number_string_1():
    do_test_number_string(x=10, expected="POSITIVE")


def test_number_string_2():
    do_test_number_string(x=-7, expected="NEGATIVE")


def test_number_string_3():
    do_test_number_string(x=0, expected="ZERO")


def test_num_divisible_1():
    do_test_num_divisible(lb=1, ub=20, p=2, q=3, expected=10)


def test_num_divisible_2():
    do_test_num_divisible(lb=2, ub=3, p=2, q=3, expected=2)


def test_num_divisible_3():
    do_test_num_divisible(lb=12, ub=20, p=2, q=2, expected=0)


def test_num_divisible_4():
    do_test_num_divisible(lb=1, ub=25, p=3, q=5, expected=11)


def test_num_divisible_5():
    do_test_num_divisible(lb=1, ub=25, p=27, q=5, expected=5)


def test_num_divisible_6():
    do_test_num_divisible(lb=1, ub=25, p=27, q=29, expected=0)


def test_count_greater_than_val_1():
    do_test_count_greater_than_val(lst=[1, 2, 3, 4], val=0, expected=4)


def test_count_greater_than_val_2():
    do_test_count_greater_than_val(lst=[-1, -2, -3, -4], val=0, expected=0)


def test_count_greater_than_val_3():
    do_test_count_greater_than_val(lst=[-1, 2, -3, 4], val=0, expected=2)


def test_count_greater_than_val_4():
    do_test_count_greater_than_val(lst=[1, 10, 11, 2, 12, 13], val=10, expected=3)


def test_count_greater_than_val_5():
    do_test_count_greater_than_val(lst=[], val=10, expected=0)
    

def test_negate_list_1():
    do_test_negate_list(lst=[1, 2, 3, 4], expected=[-1, -2, -3, -4])


def test_negate_list_2():
    do_test_negate_list(lst=[-1, -2, -3, -4], expected=[1, 2, 3, 4])


def test_negate_list_3():
    do_test_negate_list(lst=[-1, 2, -3, 4], expected=[1, -2, 3, -4])


def test_negate_list_4():
    do_test_negate_list(lst=[], expected=[])


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


def do_test_add_one_and_multiply(a, x, expected):
    recreate_msg = gen_recreate_msg(MODULE, "add_one_and_multiply", *(a, x))

    actual = se1.add_one_and_multiply(a, x)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_out_of_range(x, lb, ub, expected):
    recreate_msg = gen_recreate_msg(MODULE, "out_of_range", *(x, lb, ub))

    actual = se1.out_of_range(x, lb, ub)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_number_string(x, expected):
    recreate_msg = gen_recreate_msg(MODULE, "number_string", *(x,))

    actual = se1.number_string(x)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_num_divisible(lb, ub, p, q, expected):
    recreate_msg = gen_recreate_msg(MODULE, "num_divisible", *(lb, ub, p, q))

    actual = se1.num_divisible(lb, ub, p, q)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_count_greater_than_val(lst, val, expected):
    recreate_msg = gen_recreate_msg(MODULE, "count_greater_than_val", *(lst, val))

    actual = se1.count_greater_than_val(lst, val)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)


def do_test_negate_list(lst, expected):
    recreate_msg = gen_recreate_msg(MODULE, "negate_list", *(lst,))
    lst_copy = lst[:]

    actual = se1.negate_list(lst)

    check_none(actual, recreate_msg)
    check_type(actual, expected, recreate_msg)
    check_equals(actual, expected, recreate_msg)
    check_list_unmodified("lst", before=lst_copy, after=lst)
