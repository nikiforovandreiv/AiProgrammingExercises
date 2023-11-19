# Author: Sergei Baginskii, matriculation no. 22205148
# Implementation of DepthFirstSearch for Sudoku

from copy import deepcopy
from time import perf_counter

'''
    State is defined as the 2-dim array, which stores element in their positions:
    [[a_1, b_1, ..., i_1],
     [a_2, b_2, ..., i_2],
            ......
     [a_9, b_9, ..., i_9]]
     
     Path is defined as sequence of states, every next with one more element filled:
     [state1, state2, ...]
'''


class SudokuSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.current_state = self.initial_state

        # stores sequence of paths
        self.to_do = [[self.initial_state]]

        path = self.depth_first_search()
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

    def depth_first_search(self) -> list:
        while self.to_do:
            current_path = self.to_do.pop()
            self.current_state = current_path[-1]
            if self.is_goal():
                return current_path
            for state in self.next_states():
                if not self.is_explored(state):  # only add unexplored states
                    to_append = deepcopy(current_path)
                    to_append.append(state)
                    self.to_do.append(to_append)
        raise Exception("No path found")

    def is_explored(self, state_input: list) -> bool:
        """
        Right now this only SLOWS the program due to inefficiency of the checking.
        Since the implementation is really naive, it seems to be more efficient to
        not check if the state was already visited at all.

        Checks if the given state was already explored
        :param state_input: State to check
        """
        is_exp = False

        # compare two states element-by-element
        for path in self.to_do:
            for state in path:
                coincide = True
                for i in range(9):
                    for j in range(9):
                        if coincide and state_input[i][j] != state[i][j]:
                            coincide = False
                if coincide:
                    is_exp = True
                    break
            if is_exp:
                break

        return is_exp

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

    time_start = perf_counter()
    sudoku = SudokuSolver(starting_board)
    time_end = perf_counter()
    print(time_end - time_start)
