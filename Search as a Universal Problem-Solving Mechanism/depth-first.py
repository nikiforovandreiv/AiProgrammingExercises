from copy import deepcopy

'''
    State:
    [[a, b, c, ... , i],
     [a2, b2, c2, ..., i2],
            ......
     [a9, b9, c9, ..., i9]
'''

class SudokuSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.to_do = [[self.initial_state]]  # stores path, which store sequences of states [[st1, st2, ...], [st1, st2, ...], ...]
        path = self.depth_first_search()
        print(len(path))

    def is_allowed(self, x, y, n):
        state_to_check = self.expand(x, y, n)

        # horizontal
        for i in range(9):
            if i == x:
                continue
            if state_to_check[y][i] == n:
                return False

        # verticals
        for i in range(9):
            if i == y:
                continue
            if state_to_check[i][x] == n:
                return False

        # small squares, i - number of square,
        #                  1 2 3
        #                  4 5 6
        #                  7 8 9
        for i in range(9):
            if ((y // 3) * 3 + i // 3) == y and ((x // 3) * 3 + i % 3) == x:
                continue
            if self.current_state[(y // 3) * 3 + i // 3][(x // 3) * 3 + i % 3] == n:
                return False

        return True

    def expand(self, x, y, n):
        state = deepcopy(self.current_state)
        state[y][x] = n
        return state

    def is_goal(self):
        for row in self.current_state:
            for elem in row:
                if elem == 0:
                    return False
        return True

    def next_states(self):
        x_closest = -1
        y_closest = -1
        possibilities = []

        for i, row in enumerate(self.current_state):
            for j, elem in enumerate(row):
                if elem == 0:
                    x_closest = j
                    y_closest = i
                    break
            if x_closest != -1 or y_closest != -1:
                break

        for i in range(9):
            if self.is_allowed(x_closest, y_closest, i + 1):
                possibilities.append(self.expand(x_closest, y_closest, i + 1))

        return possibilities

    def depth_first_search(self):
        while self.to_do:
            current_path = self.to_do.pop()
            #print(f'current path: {current_path}')
            self.current_state = current_path[-1]
            #print(f'current state: {self.current_state}')
            # print(self.current_state)
            if self.is_goal():
                return current_path
            #print('not a goal')
            for state in self.next_states():
                #print(f'current state which we look {state}')
                to_append = deepcopy(current_path)
                to_append.append(state)
                #print(f'appended state {to_append}')
                self.to_do.append(to_append)




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

sudoku = SudokuSolver(starting_board)
