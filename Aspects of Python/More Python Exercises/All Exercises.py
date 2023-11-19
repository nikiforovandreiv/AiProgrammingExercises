# 4 Recursion and backtracking
# 4.9 Exercises

from copy import deepcopy


# Exercise 1
# Author: Mikita Zyhmantovich
def rev(input_element):
    if len(input_element) == 0:
        return input_element[:]
    return input_element[-1:] + rev(input_element[:-1])


# print(rev("Mango"))
# print(rev([1, 2, 3, 4]))


# Exercise 2
# Author: Andrei Nikiforov
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    elif n in memo:
        return memo[n]
    else:
        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
        return memo[n]


# print(fib())


# Exercise 3
# Author: Mikita Zyhmantovich
def nsp(x, y):
    if x == 0 or y == 0:
        return 1
    elif x < 0 or y < 0:
        return 0
    return nsp(x - 1, y) + nsp(x, y - 1)


# print(nsp(3, 2))


# Exercise 4
# Author: Andrei Nikiforov
def np(x, y, memo=None):
    if memo is None:
        memo = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
    if x == 0 and y == 0:
        return 1
    elif x < 0 or y < 0 or x > len(memo[0]) - 1 or y > len(memo) - 1:
        return 0
    elif memo[y][x] == 1:
        return 0
    elif memo[y][x] == 0:
        memo[y][x] = 1

    memo1 = deepcopy(memo)
    memo2 = deepcopy(memo)
    memo3 = deepcopy(memo)
    memo4 = deepcopy(memo)

    return np(x - 1, y, memo1) + np(x, y - 1, memo2) + np(x + 1, y, memo3) + np(x, y + 1, memo4)


# print(np(3, 2))


# Exercise 5
# Author: Andrei Nikiforov
def solve(n):
    def is_safe(board, row, col):
        for i in range(len(board)):
            if board[row][i] == 'Q':
                return False
            if row - i >= 0 and col - i >= 0 and board[row - i][col - i] == 'Q':
                return False
            if row + i < len(board) and col - i >= 0 and board[row + i][col - i] == 'Q':
                return False
        return True

    def solve_n_queens(board, col):
        if col == n:
            print_solution(board)
            return

        for row in range(n):
            if is_safe(board, row, col):
                board[row][col] = 'Q'
                solve_n_queens(board, col + 1)
                board[row][col] = '.'

    def print_solution(board):
        for row in board:
            print(' '.join(row))
        input("more?")

    solve_n_queens([['.' for _ in range(n)] for _ in range(n)], 0)


# solve(12)
