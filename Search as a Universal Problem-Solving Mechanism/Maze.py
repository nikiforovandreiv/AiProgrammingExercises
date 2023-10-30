# Author: Mikita Zyhmantovich
# Implementation of BreadthFirstSearch for Maze
import queue


class PathNotFound(BaseException):
    pass


maze = [[' ', 'W', ' ', ' ', 'G'],
        [' ', 'W', ' ', 'W', ' '],
        [' ', 'W', ' ', ' ', ' '],
        [' ', ' ', 'W', 'W', ' '],
        [' ', ' ', ' ', ' ', ' ']]


def is_goal(s):
    i, j = s[0], s[1]
    if maze[i][j] == "G":
        return True
    else:
        return False


def next_states(state):
    def allowed(s, d):
        pos_i = s[0] + d[0]
        pos_j = s[1] + d[1]
        if pos_i < 0 or pos_i >= len(maze) or pos_j < 0 or pos_j >= len(maze[0]) or maze[pos_i][pos_j] == "W":
            return False
        return True

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # directions: up, down, left, right
    return [(state[0] + d[0], state[1] + d[1]) for d in dirs if allowed(state, d)]


def breadth_first(s):
    to_do = queue.Queue()
    to_do.put([s])
    explored = [s]
    while not to_do.empty():
        path = to_do.get()
        current = path[-1]
        if is_goal(current):
            return path
        for state in next_states(current):
            if state not in explored:
                new_path = path.copy()
                new_path.append(state)
                to_do.put(new_path)
                explored.append(state)
    raise PathNotFound


try:
    startState = (len(maze) - 1, 0)
    print(breadth_first(startState))

except PathNotFound:
    print("Path not found")
