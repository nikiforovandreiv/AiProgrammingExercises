# Author: Vladyslav Chornyi

from time import time
from random import randrange, choice


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


# The heuristic function calculates the length of the longest sequence of consecutive numbers
# States with longer sequences and shorter path length are preferred
def h(path):
    state = path[-1]
    state = sum(state, start=list())

    max_length = 1
    current_length = 1
    for i in range(len(state)-1):
        if state[i+1] - state[i] == 1:
            current_length += 1
            continue
        max_length = max(max_length, current_length)
        current_length = 1

    return len(path) - max(max_length, current_length)


def AStar(state, goal):
    to_do = [[state]]
    explored = set()

    while to_do:
        path = to_do.pop(0)
        current = path[-1]

        if is_goal(current, goal):
            return path

        for next_state in next_states(current):
            state_tuple = tuple(tuple(row) for row in next_state)
            if state_tuple not in explored and state_tuple not in path:
                to_do.append(path + [next_state])
                explored.add(state_tuple)

        to_do.sort(key=h)

    return None


def breadth_first_search(state, goal):
    to_do = [[state]]
    explored = set()

    while to_do:
        path = to_do.pop(0)
        current = path[-1]

        if is_goal(current, goal):
            return path

        for next_state in next_states(current):
            state_tuple = tuple(tuple(row) for row in next_state)
            if state_tuple not in explored and state_tuple not in path:
                to_do.append(path + [next_state])
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


MAX_MOVES = 20

def random_state(size):
    state = generate_goal_state(size)
    for i in range(randrange(MAX_MOVES)):
        state = choice(next_states(state))
    return state


def test(size, num_tries):
    goal = generate_goal_state(size)
    star_time = 0
    bfs_time = 0
    star_length = 0
    bfs_length = 0
    for i in range(num_tries):
        initial = random_state(size)

        t = time()
        res_bfs = breadth_first_search(initial, goal)
        bfs_time += time() - t
        bfs_length += len(res_bfs)

        t = time()
        res_star = AStar(initial, goal)
        star_time += time() - t
        star_length += len(res_star)

    print(f"{num_tries} tests for size {size} complete\n"
          f"BFS results:\nAverage time: {bfs_time/num_tries} seconds\tAverage path length: {bfs_length/num_tries}\n"
          f"AStar results:\nAverage time: {star_time/num_tries} seconds\tAverage path length: {star_length/num_tries}\n\n")


if __name__ == "__main__":
    # initial_state = [
    #     [7, 2, 4],
    #     [5, 0, 6],
    #     [8, 3, 1]
    # ]
    # goal_state = generate_goal_state(3)
    #
    # t = time()
    # res_star = AStar(initial_state, goal_state)
    # print(f"Time spent for AStar: {time()-t} seconds")
    #
    # t = time()
    # res_bfs = breadth_first_search(state, goal_state)
    # print()
    #
    # format_result(res)

    test(3, 50)
    test(4, 20)
    test(5, 10)
