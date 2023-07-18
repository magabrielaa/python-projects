'''
Epidemic modelling

Gabriela Ayala

Functions for running a simple epidemiological simulation
'''

import random
import sys
import click

# This seed should be used for debugging purposes only!  Do not refer
# to this variable in your code.
TEST_SEED = 20170217

def has_an_infected_neighbor(city, location):
    '''
    Determine whether a person at a specific location has an infected
    neighbor in a city modelled as a ring.

    Args:
        city (list of tuples): the state of all people in the simulation
          at the start of the day
        location (int): the location of the person to check

    Returns (boolean): True, if the person has an infected neighbor,
      False otherwise.
    '''

    # The location needs to be a valid index for the city list.
    assert 0 <= location < len(city)

    # This function should only be called when the person at location
    # is susceptible to infection.
    disease_state, _ = city[location]
    
    assert disease_state == "S"
    
    # Find the left and right neighbors of the person.
    left_neighbor = city[location - 1]
    
    if location == (len(city) - 1):
        right_neighbor = city[location - location]
    else:
        right_neighbor = city[location + 1]
            
    # Find whether the left or right neighbor is infected.
    ds_left_neighbor, _ = left_neighbor
  
    ds_right_neighbor, _ = right_neighbor

    if ds_left_neighbor == "I" or ds_right_neighbor == "I":
        return True
    else:
        return False

def advance_person_at_location(city, location, days_contagious):
    '''
    Compute the next state for the person at the specified location.

    Args:
        city (list): the state of all people in the simulation at the
          start of the day
        location (int): the location of the person to check
        days_contagious (int): the number of a days a person is infected

    Returns (string, int): the disease state and the number of days
      the person has been in that state after simulating one day.

    '''
    
    ds, d = city[location]
    c = days_contagious

    if ds == 'S' and has_an_infected_neighbor(city,location):
        location = ('I',0)
    elif ds == 'S' and not has_an_infected_neighbor(city,location):
        location = ('S', d + 1)
    elif ds == 'I' and d + 1 < c:
        location = ('I', d + 1)
    elif ds == 'I' and d + 1 >= c:
        location = ('R', 0)
    elif ds == 'R':
        location = ('R', d + 1)
    elif ds == 'V':
        location = ('V', d + 1)

    return location
   

def simulate_one_day(starting_city, days_contagious):
    '''
    Move the simulation forward a single day.

    Args:
        starting_city (list): the state of all people in the simulation at the
          start of the day
        days_contagious (int): the number of a days a person is infected

    Returns (list of tuples): the state of the city after one day
    '''
    
    # Allocate space to hold the list of the new city state.
    new_city = []

    for location, _ in enumerate(starting_city):
        new_city.append(advance_person_at_location(starting_city, location, 
                                                   days_contagious))

    return new_city

def is_transmission_possible(city):
    """
    Is there at least one susceptible person who has an infected neighbor?

    Args:
        city (list): the current state of the city

    Returns (boolean): True if the city has at least one susceptible person
        with an infected neighbor, False otherwise.
    """
    
    transmission_possible = False

    for location, (ds, d) in enumerate(city):
        # Transmission possible if there is at least one susceptible
        # person who has an infected neighbor.
        if ds == 'S' and has_an_infected_neighbor(city,location):
            transmission_possible = True
            
    return transmission_possible


def run_simulation(starting_city, days_contagious):
    '''
    Run the entire simulation

    Args:
        starting_city (list): the state of all people in the city at the
          start of the simulation
        days_contagious (int): the number of a days a person is infected

    Returns tuple (list of tuples, int): the final state of the city
      and the number of days actually simulated.
    '''
    
    # Initialize at 0 the counter of days passed in the simulation.
    days_passed = 0

    while is_transmission_possible(starting_city):
        days_passed += 1
        starting_city = (simulate_one_day(starting_city, days_contagious))
      
    return starting_city, days_passed


def vaccinate_person(vax_tuple):
    '''
    Attempt to vaccinate a single person based on their current
    disease state and personal eagerness to be vaccinated.

    Args:
        vax_tuple (string, int, float): information about a person,
          including their eagerness to be vaccinated.

    Returns (string, int): a person tuple
    '''

    ds, d, e = vax_tuple
    # Allocate space for the new person_tuple.
    person_tuple = ()

    # A susceptible person is vaccinated only when the random number 
    # generated is strictly less than the eagerness to get vaccinated.
    if ds == 'S' and random.random() < e:
        person_tuple = ('V', 0)
    else:
        person_tuple = (ds, d)

    return person_tuple


def vaccinate_city(city_vax_tuples, random_seed):
    '''
    Vaccinate the people in the city based on their current state and
    eagerness to be vaccinated.

    Args:
        city_vax_tuples (list of (string, int, float) triples):
          state of all people in the simulation at the start
          of the simulation, including their eagerness to be vaccinated.
        random_seed (int): seed for the random number generator

    Returns (list of (string, int) tuples): state of the people in the
      city after vaccination
    '''
    
    # Allocate space for the list of tuples of the people in the city
    #after the vaccination.
    new_city_tuples = []

    # Set random seed.
    random.seed(random_seed)

    for vax_tuple in city_vax_tuples:
        new_city_tuples.append(vaccinate_person(vax_tuple))
        
    return new_city_tuples


def vaccinate_and_simulate(city_vax_tuples, days_contagious, random_seed):
    """
    Vaccinate the city and then simulate the infection spread

    Args:
        city_vax_tuples (list): a list with the state of the people in the city,
            including their eagerness to be vaccinated.
        days_contagious (int): the number of days a person is infected
        random_seed (int): the seed for the random number generator

    Returns (list of tuples, int): the state of the city at the end of the
      simulation and the number of days simulated.
    """
    
    city_vax_tuples = (vaccinate_city(city_vax_tuples, random_seed))

    city_vax_tuples = run_simulation(city_vax_tuples, days_contagious)
    
    return city_vax_tuples


################ Do not change the code below this line #######################

def run_trials(vax_city, days_contagious, random_seed, num_trials):
    """
    Run multiple trials of vaccinate_and_simulate and compute the median
    result for the number of days until infection transmission stops.

    Args:
        vax_city (list of (string, int, float) triples): a list with vax
            tuples for the people in the city
        days_contagious (int): the number of days a person is infected
        random_seed (int): the seed for the random number generator
        num_trials (int): the number of trial simulations to run

    Returns:
        (int) the median number of days until infection transmission stops
    """

    days = []
    for i in range(num_trials):
        if random_seed:
            _, num_days_simulated = vaccinate_and_simulate(vax_city,
                                                           days_contagious,
                                                           random_seed+i)
        else:
            _, num_days_simulated = vaccinate_and_simulate(vax_city,
                                                           days_contagious,
                                                           random_seed)
        days.append(num_days_simulated)

    # quick way to compute the median
    return sorted(days)[num_trials // 2]


def parse_city_file(filename, is_vax_tuple):
    """
    Read a city represented as person tuples or vax tuples from
    a file.

    Args:
        filename (string): the name of the file
        is_vax_tuple (boolean): True if the file is expected to contain
          (string, int) pairs.  False if the file is expected to contain
          (string, int, float) triples.

    Returns: list of tuples or None, if the file does not exist or
      cannot be parsed.
    """

    try:
        with open(filename) as f:
            residents = [line.split() for line in f]
    except IOError:
        print("Could not open:", filename, file=sys.stderr)
        return None

    ds_types = ('S', 'I', 'R', 'V')

    rv = []
    if is_vax_tuple:
        try:
            for i, res in enumerate(residents):
                ds, nd, ve = res
                num_days = int(nd)
                vax_eagerness = float(ve)
                if ds not in ds_types or num_days < 0 or \
                   vax_eagerness < 0 or vax_eagerness > 1.0:
                    raise ValueError()
                rv.append((ds, num_days, vax_eagerness))
        except ValueError:
            emsg = ("Error in line {}: vax tuples are represented "
                    "with a disease state {}"
                    "a non-negative integer, and a floating point value "
                    "between 0 and 1.0.")
            print(emsg.format(i, ds_types), file=sys.stderr)
            return None
    else:
        try:
            for i, res in enumerate(residents):
                ds, nd = res
                num_days = int(nd)
                if ds not in ds_types or num_days < 0:
                    raise ValueError()
                rv.append((ds, num_days))
        except ValueError:
            emsg = ("Error in line {}: persons are represented "
                    "with a disease state {} and a non-negative integer.")
            print(emsg.format(i, ds_types), file=sys.stderr)
            return None
    return rv


@click.command()
@click.argument("filename", type=str)
@click.option("--days-contagious", default=2, type=int)
@click.option("--task-type", default="no_vax",
              type=click.Choice(['no_vax', 'vax']))
@click.option("--random-seed", default=None, type=int)
@click.option("--num-trials", default=1, type=int)
def cmd(filename, days_contagious, task_type, random_seed, num_trials):
    '''
    Process the command-line arguments and do the work.
    '''
    city = parse_city_file(filename, task_type == "vax")
    if not city:
        return -1

    if task_type == "no_vax":
        print("Running simulation ...")
        final_city, num_days_simulated = run_simulation(
            city, days_contagious)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    elif num_trials == 1:
        print("Running one vax clinic and simulation ...")
        final_city, num_days_simulated = vaccinate_and_simulate(
            city, days_contagious, random_seed)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials of the vax clinic and simulation ...")
        median_num_days = run_trials(city, days_contagious,
                                     random_seed, num_trials)
        print("Median number of days until infection transmission stops:",
              median_num_days)
    return 0


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter
