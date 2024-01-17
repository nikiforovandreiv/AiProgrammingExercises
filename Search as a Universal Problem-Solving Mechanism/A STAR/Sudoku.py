# Author: Vladyslav Chornyi

from copy import deepcopy
from time import time


class SudokuSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.current_state = self.initial_state

        # stores sequence of paths
        self.to_do = [[self.initial_state]]

        path = self.AStar()
        print(len(path))
        self.print_board(path[-1])

    def is_allowed(self, x: int, y: int, n: int) -> bool:
        """
        Checks if it is allowed by sudoku rules to insert specified element in specified position.
        :param x: x coordinate
        :param y: y coordinate
        :param n: number to insert
        """
        state_to_check = self.expand(x, y, n)

        # horizontal fit
        for i in range(9):
            if i == x:
                continue
            if state_to_check[y][i] == n:
                return False

        # vertical fit
        for i in range(9):
            if i == y:
                continue
            if state_to_check[i][x] == n:
                return False

        # smaller squares fit, i - the number of square,
        #                  1 2 3
        #                  4 5 6
        #                  7 8 9
        for i in range(9):
            if ((y // 3) * 3 + i // 3) == y and ((x // 3) * 3 + i % 3) == x:
                continue
            if self.current_state[(y // 3) * 3 + i // 3][(x // 3) * 3 + i % 3] == n:
                return False

        return True

    def expand(self, x: int, y: int, n: int) -> list:
        state = deepcopy(self.current_state)
        state[y][x] = n
        return state

    def is_goal(self) -> bool:
        for row in self.current_state:
            for elem in row:
                if elem == 0:
                    return False
        return True

    def next_states(self) -> list:
        """
        Finds all possible states after inserting fitting element in the first available position
        :return: List of possible states on the next move
        """
        x_closest = -1
        y_closest = -1
        possibilities = []

        # find the first empty cell
        for i, row in enumerate(self.current_state):
            for j, elem in enumerate(row):
                if elem == 0:
                    x_closest = j
                    y_closest = i
                    break
            if x_closest != -1 or y_closest != -1:
                break

        # check all the possible number insertions
        for i in range(9):
            if self.is_allowed(x_closest, y_closest, i + 1):
                possibilities.append(self.expand(x_closest, y_closest, i + 1))

        return possibilities

    def AStar(self):
        visited = set()
        while self.to_do:
            current_path = self.to_do.pop()
            self.current_state = current_path[-1]
            if self.is_goal():
                return current_path
            for state in self.next_states():
                state_tuple = tuple(tuple(row) for row in state)
                if state_tuple not in visited:  # only add unexplored states
                    to_append = deepcopy(current_path)
                    to_append.append(state)
                    self.to_do.append(to_append)
                    visited.add(state_tuple)
            self.to_do.sort(key=h)
        raise Exception("No path found")

    def print_board(self, state: list) -> None:
        """
        Prints board in a well-readable format
        :param state:
        """
        to_print = ""

        for i in range(9):
            for j in range(9):
                to_print += str(state[i][j])
                to_print += ' '
                if j % 3 == 2 and j != 8:
                    to_print += '| '
            to_print += '\n'
            if i % 3 == 2 and i != 8:
                to_print += '-----   -----   -----\n'

        print(to_print)


# The heuristic function calculates "fullness" of a state,
# Meaning states that have several completely filled rows or columns are preferred
def h(path):
    factor = 9**3
    state = path[-1]
    filled = 0
    for line in state:
        num = len(list(filter(lambda x: x != 0, line)))
        filled += num**4 / factor
    for col in zip(*state):
        num = len(list(filter(lambda x: x != 0, col)))
        filled += num ** 4 / factor

    return len(path) + filled/2


if __name__ == '__main__':
    starting_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 0, 0]
    ]

    time_start = time()
    sudoku = SudokuSolver(starting_board)
    time_end = time()
    print(time_end - time_start)