# Author: Andrei Nikiforov, Oleksii Kalashnikov
# Implementation of DepthFirstSearch for n Queens

def is_goal(state, n_queens):
    return len(state) == n_queens


def allowed(state, col):
    current_row = len(state)
    return all(state[row] != col and abs(state[row] - col) != current_row - row for row in range(current_row))


def next_states(state, n_queens):
    return [state + [col] for col in range(n_queens) if allowed(state, col)]


def depth_first_search(n_queens):
    to_do = [[]]
    explored = set()

    while to_do:
        state = to_do.pop(-1)
        if is_goal(state, n_queens):
            return state

        explored.add(tuple(state))

        for state in next_states(state, n_queens):
            if tuple(state) not in explored:
                to_do.append(state)
    return None


def format_result(result):
    if result:
        for row in range(len(result)):
            row = ['Q' if col == result[row] else '.' for col in range(len(result))]
            print(' '.join(row))
    else:
        print("No solution found")


format_result(depth_first_search(10))
