"""
CS 121
Short Exercises #2
"""

def peep(p, e):
    """
    Determine whether or not peep = pp^e

    Inputs:
      p (int): first digit
      e (int): second digit

    Returns: True if peep = pp^e, False otherwise
    """

    ### EXERCISE 1 -- Replace pass with your code
    x = int (f"{p}{e}{e}{p}")
    y = int (f"{p}{p}")
    if x == y**e:
      return True
    else:
      return False

def count_target(lst, target):
  """
  Counts the number of times a target value is inside a list
  
  Inputs:
    lst (list): The list
  
  Returns (int): The count of the target value inside the list
  """
  count = 0
  for i, value in enumerate(lst):
    if value == target:
      count = count + 1
  return count
  
def has_more(lst1, lst2, target):
    """
    Determine which list contains more of the target value

    Inputs:
      lst1 (list): first list
      lst2 (list): second list
      target: the target value

    Returns: True if lst1 contains more of target, False otherwise
    """
    ### EXERCISE 2 -- Replace pass with your code
    if count_target(lst1,target) > count_target (lst2,target):
      return True
    else:
      return False


def make_star_strings(lst):
    """
    Create a list of star strings

    Input:
      lst (list of nonnegative integers): the list

    Returns: A list of strings of stars (*)
    """

    ### EXERCISE 3 -- Replace pass with your code
    lst_stars = []
    for i, value in enumerate(lst):
      lst_stars.append(value * "*")
    return lst_stars


def replace(lst, replacee, replacer):
    """
    Replace one element in a list with another

    Input:
      lst (list): the list
      replacee: the element to replace
      replacer: the element to replace replacee with

    Returns: None, modifies lst in-place
    """

    ### EXERCISE 4 -- Replace pass with your code
    for i, value in enumerate(lst):
      if value == replacee:
        lst [i] = replacer
    

def rows_and_columns_contain(lst, target):
    """
    Determines whether every row and every column of a list
      of lists contains a target value

    lst (list of lists): the list of lists
    target: the target value

    Returns: True if every row and every column of lst contains
      target, False otherwise
    """
    n = len(lst)
    condition_row = False
    condition_column = False

    for i in range(n):
        if target in lst:
            lst = [i]
            condition_row = True

    
    for i in range(n):
        for j in range(n):
            if target in lst:
                lst = [i][j]
                condition_column = True
    
    if condition_row and condition_column == True:
        return True
    else:
        return False
    



