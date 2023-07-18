"""
Language shifts

Gabriela Ayala

Functions for language shift simulation.

This program takes the following parameters:
    grid _file (string): the name of a file containing a sample region
    R (int): neighborhood radius
    A (float): the language state transition threshold A
    Bs (list of floats): a list of the transition thresholds B to
      use in the simulation
    C (float): the language state transition threshold C
      centers (list of tuples): a list of community centers in the
      region
    max_steps (int): maximum number of steps

Example use:
    $ python3 language.py -grid_file tests/writeup-grid-with-cc.txt
	  --r 2 --a 0.5 --b 0.9 --c 1.2 --max_steps 5
While shown on two lines, the above should be entered as a single command.
"""

import copy
import click
import utility

def is_sl_within_community_center(grid, centers, location):
    """
    Determines whether an SL speaking location (home) is serviced by a
    given community center.

    Inputs:
        grid (list of lists): the grid

        centers (list of tuples): inside each element of the list, there is 
        a tuple with row (i) and column (j) of the center location, the 
        second element is the distance (d) serviced by the center.

        location (tuple): tuple of two integers, the first determines
        the row and the second the column of the location.
    
    Returns (boolean): True if SL speaking home is serviced by the community
    center, False otherwise.
    """
    i, j = location

    #The function should only be called for an SL speaking location.
    assert grid[i][j] >= 1

    for ((center_row, center_column), d) in centers:
        if abs(i - center_row) <= d  and abs(j - center_column) <= d:
            return True

    return False 


def engagement_level(grid, location, R):
    """
    Computes the language engagement level of a location (home).

    Inputs:
        grid (list of lists): the grid

        location (tuple): tuple of two integers, the first determines
        the row and the second the column of the location.

        R (int): the radius of the neighborhood
    
    Returns (float): engagement level of the location
    """
    i, j = location
    sum = 0
    total_homes = 0
    
    # First, set the boundaries of the location's neighborhood.
    size = len(grid)
    lb_row = max(0, i - R)
    ub_row = min(i + R + 1, size)
    lb_col = max(0, j - R)
    ub_col = min(j + R + 1, size)

    # Compute engangement level of the location.
    for row in range(lb_row, ub_row):
        for column in range(lb_col, ub_col):
            sum += grid[row][column]
            total_homes += 1

    return sum / total_homes

def transmission_next_generation(grid, location, thresholds, R, centers):
    """
    Computes a location's language preference transmission to the next generation
    (from parents to children in a given location).

    Inputs:
        grid (list of lists): the grid

        location (tuple): tuple of two integers, the first determines
        the row and the second the column of the location.

        thresholds (tuple): tuple of three integers A, B, C containing
        the transmission thresholds.

        R (int): the radius of the neighborhood

        centers (list of tuples): inside each element of the list, there is 
        a tuple with row (i) and column (j) of the center location, the 
        second element is the distance (d) serviced by the center.
    """
    i, j = location
    A, B, C = thresholds
    E = engagement_level(grid, location, R)
    
    # The function is_sl_within_community center needs to be called only 
    # for SL speaking locations.
    if grid[i][j] >= 1:
        condition = is_sl_within_community_center(grid, centers, location)

    # Applying transmission conditions according to tresholds A, B, C.
    if grid[i][j] == 0:
        if E > B:
            grid[i][j] = 1
    elif grid[i][j] == 1 and condition:
        if C < E:
            grid[i][j] = 2
    elif grid[i][j] == 1 and not condition:
        if E < B:
            grid[i][j] = 0
        elif C < E:
            grid[i][j] = 2
    elif grid[i][j] == 2 and not condition:
        if E <= A:
            grid[i][j] = 0
        elif A < E < B:
            grid[i][j] = 1
    
def change_in_step_simulation(grid, threshold, R, centers):
    """
    Determines if there is a change in language state when taking a
    step in the language shift simulation.

    Inputs:
        grid (list of lists): the grid

        threshold (tuple): tuple of three integers A, B, C containing
        the transmission thresholds.

        R (int): the radius of the neighborhood

        a tuple with row (i) and column (j) of the center location, the 
        second element is the distance (d) serviced by the center.
    
    Returns (boolean): True if a change in language states happened
    in one step of the simulation.
    """
    change_happened = False

    previous_grid = grid
    
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            transmission_next_generation(grid, (i, j), threshold, R, centers)
            if grid[i][j] != previous_grid[i][j]:
                change_happened = True
            else:
                change_happened = False

    return change_happened


def run_simulation(grid, R, thresholds, centers, max_steps):
    """
    Do the simulation.

    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      thresholds (float, float, float): the language
        state transition thresholds (A, B, C)
      centers (list of tuples): a list of community centers in the
        region
      max_steps (int): maximum number of steps

    Returns (tuple): the frequency of each language state (int, int, int)
    """
    A, B, C = thresholds
    number_steps = 0
    change_happened = False

    # Run the simulation until the maximum number of steps is reached
    # or there is no change in the language state of any location.
    for i in range(max_steps):
        if not change_happened:
            number_steps += 1 
            change_happened = change_in_step_simulation(grid, thresholds, R, centers)
       
    # Create a list to keep track of language state counts.
    home_counts = [0]*3
    
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == 0: 
                home_counts[0] += 1
            elif column == 1:
                home_counts[1] += 1
            elif column == 2:
                home_counts[2]+= 1
         
    return grid, tuple(home_counts)
    

def simulation_sweep(grid, R, A, Bs, C, centers, max_steps):
    """
    Run the simulation with various values of threshold B.

    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      A (float): the language state transition threshold A
      Bs (list of floats): a list of the transition thresholds B to
        use in the simulation
      C (float): the language state transition threshold C
      centers (list of tuples): a list of community centers in the
        region
      max_steps (int): maximum number of steps

    Returns: a list of frequencies (tuples) of language states for
      each threshold B.
    """
    language_states = []
    
    for B in Bs:
        new_grid = copy.deepcopy(grid)
        _, freqs = run_simulation(new_grid, R, (A, B, C), centers, max_steps)
        language_states.append(freqs)
    
    return language_states


@click.command(name="language")
@click.option('--grid_file', type=click.Path(exists=True),
              default="tests/writeup-grid.txt",
              help="filename of the grid")
@click.option('--r', type=int, default=1, help="neighborhood radius")
@click.option('--a', type=float, default=0.6, help="transition threshold A")
@click.option('--b', type=float, default=0.8, help="transition threshold B")
@click.option('--c', type=float, default=1.6, help="transition threshold C")
@click.option('--max_steps', type=int, default=1,
              help="maximum number of simulation steps")
def cmd(grid_file, r, a, b, c, max_steps):
    '''
    Run the simulation.
    '''

    grid, centers = utility.read_grid(grid_file)
    print_grid = len(grid) < 20

    print("Running the simulation...")

    if print_grid:
        print("Initial region:")
        for row in grid:
            print("   ", row)
        if len(centers) > 0:
            print("With community centers:")
            for center in centers:
                print("   ", center)

    # run the simulation
    frequencies = run_simulation(grid, r, (a, b, c), centers, max_steps)

    if print_grid:
        print("Final region:")
        for row in grid:
            print("   ", row)

    print("Final language state frequencies:", frequencies)

if __name__ == "__main__":
    cmd()