import os
import sys

import json
import pytest

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

import se4

MODULE = "battleship"

fleet_configs = \
  {"full_fleet": {'Carrier': (0, 4),
                  'Battleship': (1, 0),
                  'Destroyer': (3, 2),
                  'Submarine': (6, 4),
                  'Patrol Boat': (9, 8)},
   "one_ship": {'Carrier': (4, 4)},
   "two_ships_same_row": {'Carrier': (4, 1),
                          'Patrol Boat': (4, 7)},
   "two_adjacent_ships": {'Carrier': (4, 0),
                               'Patrol Boat': (4, 5)},
   "no_ships": {}
   }

move_configs = \
    [("one_ship", [(4, 6)]),
     ("one_ship", [(4, 0)]),
     ("one_ship", [(4, 6), (4, 5), (4, 4), (4, 3), (4, 7), (4, 8)]),
     ("full_fleet", [(9, 8), (9, 7), (9, 9)]),
     ("full_fleet", [(1, 0), (1, 1), (1, 2), (1, 3)]),
     ("two_ships_same_row", [(4, x) for x in range(10)]),
     ("two_adjacent_ships", [(4, x) for x in range(10)]),
     ("no_ships", [(x, x) for x in range(10)]),
     ("full_fleet", [])
    ]

ALL_WATER = json.load(open("tests/no_ships.json"))["board"] 

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
    msg = "Actual ({}) and expected ({}) values do not match.".format(actual, expected)
    if recreate_msg is not None:
        msg += "\n" + recreate_msg

    assert actual == expected, msg

def check_boards_same(actual, expected, recreate_msg):
    if actual == expected:
        return

    msg = ("Actual number of rows ({}) does"
           " not equal the expected number of rows ({})\n")
    msg = msg.format(len(actual), len(expected))
    assert len(actual) == len(expected), msg + recreate_msg


    for i, expected_row in enumerate(expected):
        msg0 = ("Wrong type for element {}."
                " Expected type: list.  Got type: {}\n".format(i, type(actual[i])))
        check_type(actual[i], expected_row, msg0 + recreate_msg)

        msg1 = ("Actual number of columns in row {} ({})"
                " does not equal the expected number"
                " of columns ({})")
        msg1 = msg1.format(i, len(actual[i]), len(expected_row))
        assert len(actual[i]) == len(expected_row), \
            msg1 + recreate_msg

        msg2 = "Mismatch in row {}\n"
        msg2 += "    Actual row:   {}\n"
        msg2 += "    Expected row: {}\n\n"
        msg2 += recreate_msg
        assert actual[i] == expected_row, \
            msg2.format(i,
                        " ".join([v[0] for v in actual[i]]),
                        " ".join([v[0] for v in expected_row]))
        
    
def check_board(actual, expected_board, expected_num_ships, recreate_msg):
    check_attribute(actual, "board", recreate_msg)
    check_attribute_type(actual.board,
                         expected_board,
                         recreate_msg)

    check_attribute(actual, "num_ships", recreate_msg)
    check_attribute_type(actual.num_ships,
                         expected_num_ships,
                         recreate_msg)
    
    check_boards_same(actual.board, expected_board, recreate_msg)
    

def board_helper(file_prefix, add_fleet=True):
    filename = "tests/{}.json".format(file_prefix)
    with open(filename) as f:
        config = json.load(f)

    recreate_msg = "To recreate this test run:\n"
    recreate_msg += "    board = se4.Board()\n"

    actual = se4.Board()
    check_board(actual, ALL_WATER, 0, recreate_msg)

    if add_fleet:
        recreate_msg += "    config = json.load(open('{}'))\n"
        recreate_msg += "    board.deploy_fleet(config['ships'])\n"
        recreate_msg = recreate_msg.format(filename)
        actual.deploy_fleet(config["ships"])

        check_board(actual, config["board"], len(config["ships"]), recreate_msg)

        

    return config, actual, recreate_msg


def test_constructor():
    board_helper("no_ships", False)


@pytest.mark.parametrize(
    "fleet_name",
    fleet_configs)
def test_deploy_fleet(fleet_name):
    board_helper(fleet_name)
    


@pytest.mark.parametrize(
    "fleet_name",
    fleet_configs)
def test_str(fleet_name):
    config, board, recreate_msg = board_helper(fleet_name, False)
    recreate_msg += "    str(board)\n"

    # Hack: swap in the expected board
    board.board = config["board"]

    actual = str(board)
    check_none(actual, recreate_msg)
    check_type(actual, config["str"], recreate_msg)
    check_equals(actual, config["str"], recreate_msg)

@pytest.mark.parametrize(
    "fleet_name",
    fleet_configs)
def test_is_over(fleet_name):
    config, board, recreate_msg = board_helper(fleet_name)
    recreate_msg += "    board.is_game_over()\n"
    actual = board.is_game_over()
    check_none(actual, recreate_msg)
    check_type(actual, config["is_over"], recreate_msg)
    check_equals(actual, config["is_over"], recreate_msg)
    
    
@pytest.mark.parametrize(
    "test_num",
    range(len(move_configs)))
def test_play_move(test_num):
    filename = "tests/moves_{}.json".format(test_num)
    config, board, recreate_msg = board_helper("moves_{}".format(test_num))

    for loc, expected in zip(config["moves"], config["expected_results"]):
        recreate_msg += "    board.play_move({})".format(loc)
        actual = board.play_move(loc)
        check_none(actual, recreate_msg + "    # Failed here")
        check_type(actual, expected, recreate_msg  + "    # Failed here")
        check_equals(actual, expected, recreate_msg  + "    # Failed here")
        recreate_msg += "\n"

    check_boards_same(board.board, config["final_board"], recreate_msg)
    check_equals(board.num_ships, config["num_ships"], recreate_msg)


    
