
def engagement_level(grid, location, R):
    i, j = location
    neighborhood = []

    for i_row, row in enumerate(grid):
        if (i_row == i) or (i <= i_row <= i + R) or (i > i_row >= i - R):
            for j_column, column in enumerate(row):
                if (j_column == j) or (j <= j_column <= j + R) or (j > j_column >= j - R):
                    neighborhood.append(column)
    
    S = sum(neighborhood)
    E = S / (len(neighborhood))

    return E

