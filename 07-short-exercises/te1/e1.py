def predicted_coins(max_per_side, guesses_to_win, seq):
    
    num_correct_guesses = 0
    friend_wins = False

    for i, (actual, guess) in enumerate(seq):
        if actual == guess:
            num_correct_guesses += 1
        if i == max_per_side and num_correct_guesses >= guesses_to_win:
            friend_wins = True

    return friend_wins 

def champions(ledger, threshold, num_champs):
    assert threshold > 0

    d = {}
    winners = []
    champ = 0

    for house, points in ledger:
        if house not in d:
            d[house] = points
        elif house in d:
            accumulated_pts = d[house] + points
            d[house] = accumulated_pts
        if d[house] >= 100 and champ < num_champs and house not in winners:
            winners.append(house)
            champ += 1
            
    return winners


# Timed Exercise 2.1: Lists/Dictionaries/Sets/Functions 

def get_columns(rows):
    #Initialize empty set
    columns = set()

    for row in rows:
        for col in row:
            columns.add(col)

    return columns

def fill_missing(rows, default_values=None):

    columns = get_columns(rows)

    for col in columns:
        for row in rows:
            if col not in row and default_values != None:
                row[col] = default_values[col] 
            elif col not in row and default_values == None:
                row[col] = None
    
        


students = [{"first_name": "A1", "last_name": "A2"},
            {"first_name": "B1", "last_name": "B2", "student_id": 123},
            {"first_name": "C1", "last_name": "C2", "cnetid": "C3"}]

directory = [{"name": "Prof. A", "phone": "773-555-1234", "email": "a@example.org"},
             {"name": "Prof. B", "email": "a@example.org"},
             {"name": "Prof. C"},
             {"name": "Prof. D", "phone": "773-555-4321", "email": "d@example.org"}]

things = [{"foo": 42},
          {"bar": 37},
          {"baz": 23},
          {"qux": 10}]


