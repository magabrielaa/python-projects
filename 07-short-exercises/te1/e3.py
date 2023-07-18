def flip(lst):
    # Define the number of rows for the new list
    range_lst = []
    for i, val in enumerate(lst):
        range_lst.append(i)
    max_range = max(range_lst)

    new_lst = []
    for num in range(max_range):
        new_row = []
        for i, row in enumerate(lst):
            for j, column in enumerate(row):
                assert 0 <= i + 1 <= (max_range - 1)
                new_row.append(lst[i + 1][j])
        new_lst.append(new_row)
    return new_lst
            

    