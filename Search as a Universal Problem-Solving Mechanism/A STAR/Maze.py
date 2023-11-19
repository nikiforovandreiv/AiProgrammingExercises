# Author: Mikita Zyhmantovich
# A* implementation to solve the Maze puzzle
import math


class PathNotFound(BaseException):
    pass


maze = [[' ', 'W', ' ', ' ', 'G'],
        [' ', 'W', ' ', 'W', ' '],
        [' ', 'W', ' ', ' ', ' '],
        [' ', ' ', 'W', 'W', ' '],
        [' ', ' ', ' ', ' ', ' ']]


def findGoal():
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == "G":
                return i, j
    raise PathNotFound


def isGoal(s):
    i, j = s[0], s[1]
    if maze[i][j] == "G":
        return True
    else:
        return False


def nextStates(s):
    def allowed(s, d):
        pos_i = s[0] + d[0]
        pos_j = s[1] + d[1]
        if pos_i < 0 or pos_i >= len(maze) or pos_j < 0 or pos_j >= len(maze[0]) or maze[pos_i][pos_j] == "W":
            return False
        return True

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # directions: up, down, left, right
    return [(s[0] + d[0], s[1] + d[1]) for d in dirs if allowed(s, d)]


def aStarSearch(s):
    goal = findGoal()

    def h(path):
        return abs(path[-1][0] - goal[0]) + abs(path[-1][1] - goal[1])

    toDo = [[s]]
    explored = [s]
    while len(toDo) != 0:
        toDo.sort(key=h, reverse=True)
        path = toDo.pop()
        current = path[-1]
        if isGoal(current):
            return path
        for state in nextStates(current):
            if state not in explored:
                new_path = path.copy()
                new_path.append(state)
                toDo.append(new_path)
                explored.append(state)
    raise PathNotFound


try:
    startState = (len(maze) - 1, 0)
    print(aStarSearch(startState))

except PathNotFound:
    print("Path not found")
