'''
Short Exercises #5
'''

import numpy as np

def compute_matching(x, y):
    """
    Returns a new array which is "true" everywhere x == y and
    false otherwise.

    Note this is simply the Numpy version of the same function
    in SE2 but should be substantially simpler.

    Input:
        x: n-dimensional array
        y: n-dimensional array

    Returns: Boolean-valued n-dimensional array with the same shape as
             x and y
    """
     
    return x == y


def compute_matching_indices(x, y):
    """
    Returns a new array consisting of the indices where
    x == y.

    Note this is simply the Numpy version of the same function
    in SE2 but should be substantially simpler.

    Input:
        x: 1-dimensional array
        y: 1-dimensional array

    Returns: a sorted array of the indices where x[i] == y[i]

    Note that the returned array must be one-dimensional!

    """
    z = np.argwhere(x == y)

    return z.flatten()


def powers(N, p):
    """
    Return the first N powers of p. For example:
    powers(5, 2) --> [1, 2, 4, 8, 16]
    powers(5, 4) --> [1, 4, 16, 64, 256]

    Input:
       N: number of powers to return
       p: base that we are raising to the given powers

    Returns: an array consisting of powers of p
    """

    power_array = np.arange(N)
    N_array = np.array(p)

    rv = N_array ** power_array

    return rv


def clip_values(x, min_val=None, max_val=None):
    """
    Return a new array with the values clipped.

    If min_val is set, all values < min_val will be set to min_val
    If max_val is set, all values > max_val will be set to max_val

    Remember to return a new array, NOT to modify the input array.

    Inputs:
        x: the n-dimensional array to be clipped
        min_val : the minimum value in the returned array (if not None)
        max_val : the maximum value in the returned array (if not None)

    returns: an array with the same dimensions of X with values clipped
             to (min_val, max-val)

    """
    z = np.copy(x)

    if min_val is not None and max_val is None:
       z[z < min_val] = min_val
    elif max_val is not None and min_val is None:
        z[z > max_val] = max_val
    elif min_val is not None and max_val is not None:
        z[z < min_val] = min_val
        z[z > max_val] = max_val

    return z

def find_closest_value(x):
    """
    Returns the index and corresponding value in the one-dimensional
    array x that is closest to the mean

    Examples:
    find_closest_value(np.array([1.0, 2.0, 3.0])) -> (1, 2.0)
    find_closest_value(np.array([5.0, 1.0, 8.0])) -> (0, 5.0)

    Inputs:
        x: 1-dimensional array of values

    Returns: the index and the scalar value in x that is
        closest to the mean

    """
    mean = np.mean(x)
    abs_val = np.absolute(x - mean)
    closest_i= np.argmin(abs_val)

    return closest_i, x[closest_i]


def select_row_col(x, row_idx=None, col_idx=None):
    """
    Select a subset of rows or columns in the two-dimensional array x.

    Inputs:
        x: input two-dimensional array
        row_idx: a list of row index we are selecting, None if not specified
        col_idx: a list of column index we are selecting, None if not specified

    Returns: a two-dimensional array where we have selected based on the
        specified row_idx and col_idx
    """

    if col_idx is None and row_idx is not None:
        y = x[(row_idx)]
    elif row_idx is None and col_idx is not None:
        y = x[:,col_idx]
    elif col_idx is not None and row_idx is not None:
        y = x[row_idx][:,col_idx]
    else:
        y = np.copy(x)

    return y


