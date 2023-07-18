'''
Polling places

Utilities
'''

import json
import random
import sys

# DO NOT MODIFY THIS FILE
# pylint: disable-msg= invalid-name, too-many-arguments, line-too-long
# pylint: disable-msg= too-many-branches

def gen_voter_parameters(arrival_rate, voting_duration_rate,
                         impatience_prob):
    '''
    Draw gap and voting duration from exponetial distribution

    Inputs:
        arrival_rate: (float) Lambda for gap
        voting_duration_rate: (float) Lambda for voting duration
        impatience_prob: (float) probability that the voter will be impatient.

    Returns:
        (gap, voting duration, is_impatient) two floats and a boolean
    '''

    voting_duration = random.expovariate(voting_duration_rate)
    gap = random.expovariate(arrival_rate)
    is_impatient = (random.random() <= impatience_prob)

    return (gap, voting_duration, is_impatient)


def load_precinct(precinct_filename):
    '''
    Load a precinc file.

    Inputs:
        precinct_filename: (string) Name of the precinct file

    Returns:
        A tuple containing:
        - a precinct dictionary
        - a seed (integer)
    '''

    try:
        config = json.load(open(precinct_filename))
    except OSError as e:
        print("{}".format(e), file=sys.stderr)
        return None

    if not isinstance(config, dict):
        raise ValueError("Configuration file syntax error: should contain a JSON object")

    # Validate seed
    if "seed" not in config or not isinstance(config["seed"], int):
        raise ValueError("Configuration file syntax error: does not contain a seed")

    # Validate precinct
    if "precinct" not in config or not isinstance(config["precinct"], dict):
        raise ValueError("Configuration file syntax error: does not contain a precinct")

    precinct = config["precinct"]
    if "name" not in precinct:
        raise ValueError("Precinct is missing 'name' field: {}".format(p))

    for f in ("hours_open", "num_voters", "voting_duration_rate",
              "arrival_rate", "impatience_prob"):
        if f not in precinct:
            raise ValueError("Precinct {} is missing '{}' field".format(p["name"], f))

    return precinct, config["seed"]



def print_voters(voters, filename=None, line_prefix=""):
    '''
    Print the voters generated by the simulation.

    Inputs:
      voters: A list of voter objects
      filename: (string) Specifies the name of a file to use,
         if included.
      line_prefix: (string) String to prepend to the output lines
        (used to generate the output for the writeup)
    '''
    if filename is None:
        file = sys.stdout
    else:
        try:
            file = open(filename, "w")
        except OSError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    s =  "{}Arrival        Voting             Is             Start         Departure          Has\n"
    s += "{}Time           Duration           Impatient      Time          Time               Voted\n"
    s += "{}---------------------------------------------------------------------------------------"
    print(s.format(line_prefix, line_prefix, line_prefix), file=file)
    for v in voters:
        s = "{:8.2f}"
        none_str = "    None"
        at = "{:5.2f}".format(v.arrival_time) if v.arrival_time else none_str
        vd = s.format(v.voting_duration) if v.voting_duration else none_str
        st = s.format(v.start_time) if v.start_time else none_str
        dt = s.format(v.departure_time) if v.departure_time else none_str
        hv = "       T" if v.has_voted else "       F"
        imp ="       T" if v.is_impatient else "       F"
        combined = "{}{}       {}         {}          {}      {}       {}\n"
        print(combined.format(line_prefix, at, vd, imp, st, dt, hv), file=file)
