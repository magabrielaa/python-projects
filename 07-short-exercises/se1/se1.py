"""
Short Exericses #1
"""


def add_one_and_multiply(a, x):
    """ Add 1 to a, and multiply by x"""

    ### EXERCISE 1 -- YOUR CODE GOES HERE
    # Replace "None" with the correct expression
    r = (1 + a) * x

    return r


def out_of_range(x, lb, ub):
    """ Is x outside the range lb to ub (inclusive)?"""

    ### EXERCISE 2 -- YOUR CODE GOES HERE
    # Replace "None" with the correct expression
    r = x < lb or x > ub

    return r


def number_string(x):
    """
    Given a number x, produce a string: "POSITIVE", "NEGATIVE", "ZERO"
    (depending on whether the number is positive, negative, or zero)
    """

    ### EXERCISE 3 -- YOUR CODE GOES HERE
    # Replace the following line with your code.
    # After running your code, variable s should contain the value
    # we ask you to compute in this exercise.
    s = "POSITIVE" if x > 0 else "NEGATIVE" if x <0 else "ZERO"

    return s


def num_divisible(lb, ub, p, q):
    """
    How many numbers between lb and ub (inclusive) are divisible by p
    or divisible by q, but not divisible by both p and q.
    """

    ### EXERCISE 4 -- YOUR CODE GOES HERE
    # Replace the following line with your code.
    # After running your code, variable n should contain the value
    # we ask you to compute in this exercise.
    n = count = sum (1 for i in list(range(lb,ub+1)) if (i % q == 0 and i % p != 0) or (i % p == 0 and i % q != 0))

    return n


def count_greater_than_val(lst, val):
    """
    Count the number of numbers in the list that are strictly greater than the value of val.
    """

    ### EXERCISE 5 -- YOUR CODE GOES HERE
    # Replace the following line with your code.
    # After running your code, variable n should contain the value
    # we ask you to compute in this exercise.
    n = count = sum (1 for i in lst if i>val)

    return n


def negate_list(lst):
    """
    Produce a *new* list with its values negated
    """

    ### EXERCISE 6 -- YOUR CODE GOES HERE
    # Replace the following line with your code.
    # After running your code, variable n should contain the value
    # we ask you to compute in this exercise
    new_lst = [-i for i in lst]

    return new_lst
