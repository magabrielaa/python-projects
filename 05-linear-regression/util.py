'''
Utility functions for linear regression assignment
'''

import json
import os.path
import sys
import numpy as np

# pylint: disable-msg= invalid-name, too-few-public-methods, no-member

def prepend_ones_column(A):
    '''
    Add a ones column to the left side of an array.
    '''

    ones_col = np.ones((A.shape[0], 1))
    return np.hstack([ones_col, A])


def linear_regression(X, y):
    '''
    Compute linear regression. Finds model, beta, that minimizes
    X beta - Y in a least squared sense.

    Accepts inputs with type array
    Returns beta, which is used only by apply_beta

    Examples
    --------
    In [1]: import numpy as np

    In [2]: from util import *

    In [3]: features = np.array([[5, 2], [3, 2], [6, 2.1], [7, 3]]) # features

    In [4]: X = prepend_ones_column(features)

    In [5]: X
    Out[5]:
    array([[1. , 5. , 2. ],
           [1. , 3. , 2. ],
           [1. , 6. , 2.1],
           [1. , 7. , 3. ]])

    In [6]: y = np.array([5, 2, 6, 6]) # observations of target variable

    In [7]: beta = linear_regression(X, y)

    In [8]: beta # yhat_n = 1.2 + 1.4 * x_n1 - 1.7 * x_n2
    Out[8]: array([ 1.20104895,  1.41083916, -1.6958042 ])

    In [9]: apply_beta(beta, X)
    Out[9]: array([4.86363636, 2.04195804, 6.1048951 , 5.98951049])
    '''

    assert_Xy(X, y, fname='linear_regression')

    # Do actual computation
    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    return beta


def load_json_file(dir_path, filename):
    '''
    Load a JSON file and return its contents.

    Inputs:
        dir_path: (string) path to the directory that contains the file
        filename: (string) name of the file

    Returns: depends on the contents of the JSON file.
    '''

    data = None

    try:
        path = os.path.join(dir_path, filename)
        with open(path) as f:
            data = json.load(f)
    except IOError as ioe:
        print("Could not open file:", filename, file=sys.stderr)
        raise ioe
    except json.JSONDecodeError as je:
        print("JSON load failed:", filename, file=sys.stderr)
        print(je)
        raise je

    return data


def load_numpy_array(dir_path, filename):
    '''
    Load a CSV file into a Numpy array and return it.

    Inputs:
        dir_path: (string) path to the directory that contains the file
        filename: (string) name of the file

    Returns: list of strings, 2D Numpy array of floats
    '''

    labels, data = None, None

    try:
        path = os.path.join(dir_path, filename)
        with open(path) as f:
            # first row must contain the column labels
            labels = f.readline().strip().split(',')
            data = np.loadtxt(f, delimiter=',', dtype=np.float64)
    except IOError:
        print("Could not open file:", filename, file=sys.stderr)
        sys.exit(0)
    except ValueError as ve:
        print("Numpy load failed:", filename, file=sys.stderr)
        print(ve)
        sys.exit(0)

    return labels, data


def apply_beta(beta, X):
    '''
    Apply beta values and feature matrix X in the linear_regression function and 
    calculate the predictions: y_{hat} = X*beta.

    Inputs:
      beta: beta values in the linear_regression
      Xs: feature matrix, 2D array of floats

    Returns:
      y_{hat}: the result of applying beta to the data, as an array.

      Given:
        beta = array([B0, B1, B2, ..., BK])
        X = array([[1, x11, x12, ..., x0K],
                   [1, x21, x22, ..., x1K],
                   ...
                   [1, xN1, xN2, ..., xNK]])

      result will be:
        array([B0+B1*x11+B2*x12+...+BK*x1K,
               B0+B1*x21+B2*x22+...+BK*x2K,
               ...
               B0+B1*xN1+B2*xN2+...+BK*xNK])
    '''

    assert_Xbeta(X, beta, fname='apply_beta')

    # Calculate X*beta
    yhat = np.dot(X, beta)
    return yhat


class Asserter:
    '''
    Helper functor to test assertions.
    '''

    def __init__(self, fname):
        self._fname = fname

    def __call__(self, cond, string, **kwargs):
        assert cond, self._fname+": "+string.format(**kwargs)


def assert_X(X, fname=''):
    '''
    Checks correctness of the shape of X and raises an assertion if it does not
    conform.
    '''

    _assert = Asserter(fname)
    _assert(isinstance(X, np.ndarray),
            "X must be a numpy array. Got type {type}.",
            type=type(X).__name__)

    _assert(X.ndim == 2,
            "X must have 2 dimensions. Got {ndim}.",
            ndim=X.ndim)


def assert_X_multicollinearity(X, fname=''):
    '''
    Checks if X has multicollinearity. This will be common if the same
    column is included twice.
    '''

    _assert = Asserter(fname)
    if X.shape[1] > 0:
        _assert(np.linalg.cond(np.dot(X.T, X)) < 1e10,
                "Did you include the same column twice? "
                "Perfect multicollinearity detected in X.")


def assert_y(y, fname=''):
    '''
    Checks correctness of y and raises an assertion if it does not conform.
    '''

    _assert = Asserter(fname)
    _assert(isinstance(y, np.ndarray),
            "y must be a numpy array. Got type {type}.",
            type=type(y).__name__)

    _assert(y.ndim == 1,
            "y must have 1 dimension. Got {ndim}.",
            ndim=y.ndim)


def assert_Xy(X, y, fname=''):
    '''
    Checks the correctness of X and y together in context of fitting a model.
    '''

    _assert = Asserter(fname)
    assert_X(X, fname=fname)
    assert_y(y, fname=fname)

    _assert(X.shape[0] == y.shape[0],
            "X and y must have the same length along axis 0. "
            "X had length {xlen} and y had length {ylen}.",
            xlen=X.shape[0],
            ylen=y.shape[0])

    assert_X_multicollinearity(X, fname=fname)


def assert_Xbeta(X, beta, fname=''):
    '''
    Checks the correctness of X and beta together.
    '''

    assert_X(X, fname=fname)

    def _assert(cond, string, **kwargs):
        assert cond, fname+": "+string.format(**kwargs)

    _assert(isinstance(beta, np.ndarray),
            "beta must be a numpy array. Got type {type}.",
            type=type(beta).__name__)

    _assert(beta.ndim == 1,
            "beta must have 1 dimensions. Got {ndim}.",
            ndim=beta.ndim)

    _assert(X.shape[1] == beta.shape[0],
            "X must have as many columns as the length of beta. "
            "X had {xcol} column(s) and beta had length {betalen}.",
            xcol=X.shape[1],
            betalen=beta.shape[0])
