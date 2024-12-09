from collections import defaultdict


class Pydoku:
    def __init__(self, grid_str: list[list[int]]):
        if len(grid_str) != 81:
            raise ValueError("Grid string must be 81 characters long")

        self.grid_str = grid_str
        self.values = []
        self.rows = "ABCDEFGHI"
        self.columns = "123456789"
        self.boxes = self.cross(self.rows, self.columns)
        self.initial_grid = {box: value for box, value in zip(self.boxes, self.grid_str)}
        self.grid = self.grid_values()
        """
        Boxes:

        ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
        'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
        'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
        """
        self.row_units = [
            self.cross(r, self.columns) for r in self.rows
        ]  # row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
        self.column_units = [
            self.cross(self.rows, c) for c in self.columns
        ]  # column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
        self.square_units = [
            self.cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")
        ]  # square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        self.unitlist = self.row_units + self.column_units + self.square_units
        self.units = self.extract_units()
        self.peers = self.extract_peers()

    def cross(self, a, b):
        return [s + t for s in a for t in b]

    def extract_units(self):
        units = defaultdict(list)
        for box in self.boxes:
            for unit in self.unitlist:
                if box in unit:
                    units[box].append(unit)
        return units

    def extract_peers(self):
        peers = defaultdict(set)

        for box in self.boxes:
            for unit in self.units[box]:
                for peer in unit:
                    if peer != box:
                        peers[box].add(peer)
        return peers

    def display(self, grid):
        """Display the values as a 2-D grid.

        Parameters
        ----------
            values(dict): The sudoku in dictionary form
        """
        width = 1 + max(len(grid[s]) for s in self.boxes)
        line = "+".join(["-" * (width * 3)] * 3)
        for r in self.rows:
            print("".join(grid[r + c].center(width) + ("|" if c in "36" else "") for c in self.columns))
            if r in "CF":
                print(line)
        print()

    def grid_values(self):
        for c in self.grid_str:
            if c == ".":
                self.values.append("123456789")
            else:
                self.values.append(c)

        return {box: value for box, value in zip(self.boxes, self.values)}

    def elimitate(self, grid):
        solved_values = [box for box in grid.keys() if len(grid[box]) == 1]

        for box in solved_values:
            digit = grid[box]
            for peer in self.peers[box]:
                grid[peer] = grid[peer].replace(digit, "")

        return grid

    def only_choice(self, grid):
        for unit in self.unitlist:
            for digit in "123456789":
                dplaces = [box for box in unit if digit in grid[box]]
                if len(dplaces) == 1:
                    grid[dplaces[0]] = digit
        return grid

    def reduce(self, grid):
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_values_before = len([box for box in grid.keys() if len(grid[box]) == 1])

            # Eliminate Strategy
            self.elimitate(grid)

            # Only Choice Strategy
            self.only_choice(grid)

            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in grid.keys() if len(grid[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in grid.keys() if len(grid[box]) == 0]):
                return False

        return grid

    def search(self, grid):
        # First, reduce the puzzle using the previous function
        values = self.reduce(grid)

        if values is False:
            return False  ## Failed earlier

        if all(len(values[s]) == 1 for s in self.boxes):
            return values  ## Solved!
        # Choose one of the unfilled squares with the fewest possibilities
        n, s = min((len(values[s]), s) for s in self.boxes if len(values[s]) > 1)
        # Now use recurrence to solve each one of the resulting sudokus, and
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt

    def solve(self):
        print("Initial grid:")
        self.display(self.initial_grid)
        self.grid = self.search(self.grid)
        print("Solved grid:")
        self.display(self.grid)


if __name__ == "__main__":
    # grid = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    grid2 = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
    pydoku = Pydoku(grid2)
    pydoku.solve()
