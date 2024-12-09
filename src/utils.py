def display(values):
    """Display the values as a 2-D grid.

    Parameters
    ----------
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = "+".join(["-" * (width * 3)] * 3)
    for r in rows:
        print("".join(values[r + c].center(width) + ("|" if c in "36" else "") for c in cols))
        if r in "CF":
            print(line)
    print()
