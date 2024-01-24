# Author: Oleksii Kalashnikov 22209805
# Implementation of A* for n Queens

import heapq

def is_goal(state, n_queens):
    return len(state) == n_queens

def heuristic(state):
    # heuristic: number of conflicts
    conflicts = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def allowed(state, col):
    current_row = len(state)
    return all(state[row] != col and abs(state[row] - col) != current_row - row for row in range(current_row))

def next_states(state, n_queens):
    return [state + [col] for col in range(n_queens) if allowed(state, col)]

def a_star_search(n_queens):
    initial_state = []
    heapq.heappush(initial_state, (heuristic([]), []))
    explored = set()

    while initial_state:
        _, state = heapq.heappop(initial_state)
        if is_goal(state, n_queens):
            return state

        explored.add(tuple(state))

        for next_state in next_states(state, n_queens):
            if tuple(next_state) not in explored:
                cost = len(next_state) + heuristic(next_state)
                heapq.heappush(initial_state, (cost, next_state))
    return None

def format_result(result):
    if result:
        for row in range(len(result)):
            row = ['Q' if col == result[row] else '.' for col in range(len(result))]
            print(' '.join(row))
    else:
        print("No solution found")

format_result(a_star_search(10))
