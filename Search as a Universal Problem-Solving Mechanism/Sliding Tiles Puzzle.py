# Author: Andrei Nikiforov
# Implementation of BreadthFirstSearch for Sliding Tiles Puzzle
# s = state
# d = direction

def generate_goal_state(n):
    return [[i * n + j for j in range(n)] for i in range(n)]


def is_goal(state, goal):
    return state == goal


def find0(state):
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] == 0:
                return row, col


def move(state, direction):
    pos_x, pos_y = find0(state)
    new_pos_x, new_pos_y = pos_x + direction[0], pos_y + direction[1]

    if 0 <= new_pos_x < len(state) and 0 <= new_pos_y < len(state[0]):
        new_state = [list(row) for row in state]
        new_state[pos_x][pos_y], new_state[new_pos_x][new_pos_y] = new_state[new_pos_x][new_pos_y], new_state[pos_x][pos_y]
        return new_state

    return None


def allowed(state, direction):
    return move(state, direction) is not None


def next_states(state):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [move(state, d) for d in dirs if allowed(state, d)]


def breadth_first_search(state, goal):
    to_do = [[state]]
    explored = set()

    while to_do:
        path = to_do.pop(0)
        current = path[-1]

        if is_goal(current, goal):
            return path

        for state in next_states(current):
            state_tuple = tuple(tuple(row) for row in state)
            if state_tuple not in explored and state_tuple not in path:
                to_do.append(path + [state])
                explored.add(state_tuple)

    return None


def format_result(result):
    if result:
        for step, state in enumerate(result):
            print(f"Step {step + 1}:")
            for row in state:
                print(row)
            print("\n")
    else:
        print("FAILURE: NO PATH FOUND")


initial_state = [
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
]
goal_state = generate_goal_state(3)

format_result(breadth_first_search(initial_state, goal_state))
