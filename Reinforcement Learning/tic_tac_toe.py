# Authors: Mikita Zyhmantovich, Andrei Nikiforov
# Implementation of Menace algorithm for Tic Tac Toe game
# Placement information

# | _ | _ | _ |
# | _ | _ | _ | = '_________'
# | _ | _ | _ |

# PLacement index
# | 0 | 1 | 2 |
# | 3 | 4 | 5 | = '012345678'
# | 6 | 7 | 8 |

# Symmetries (90 degree turns)

# | 6 | 3 | 0 |
# | 7 | 4 | 1 | = '630741852'
# | 8 | 5 | 2 |

# | 8 | 7 | 6 |
# | 5 | 4 | 3 | = '876543210'
# | 2 | 1 | 0 |

# | 2 | 5 | 8 |
# | 1 | 4 | 7 | = '258147036'
# | 0 | 3 | 6 |

import random


def win_check(board, player):  # Author: Andrei Nikiforov
    # Rows and Columns
    for i in range(3):
        # Rows
        if all(board[i * 3 + j] == player for j in range(3)):
            return True
        # Columns
        if all(board[j * 3 + i] == player for j in range(3)):
            return True

    # Top-Left to Bottom-Right Diagonals
    if all(board[i * 3 + i] == player for i in range(3)):
        return True
    # Bottom-Left to Top-Right Diagonals
    if all(board[i * 3 + 2 - i] == player for i in range(3)):
        return True

    return False


def find_symmetries(state):  # Author: Mikita Zyhmantovich. Feature was not fully implemented and therefore removed
    symmetries = []
    symmetry = ""
    for i in range(6, len(state)):
        symmetry += state[i] + state[i - 3] + state[i - 6]
    symmetries.append(symmetry)
    symmetry = ""
    for i in range(len(state)-1, -1, -1):
        symmetry += state[i]
    symmetries.append(symmetry)
    symmetry = ""
    for i in range(2, -1, -1):
        symmetry += state[i] + state[i + 3] + state[i + 6]
    symmetries.append(symmetry)
    return symmetries


def is_final(state):  # Author: Mikita Zyhmantovich
    if not win_check(state, 'X') and not win_check(state, 'O'):  # if X didn't win as well as O and board is full then
        for char in state:  # it's a draw
            if char == '_':
                return False
    return True  # some player won, so the state is final


def place(board, position): # Author: Andrei Nikiforov
    if board.count('X') > board.count('O'):
        player = 'O'
    else:
        player = 'X'

    return board[:position] + player + board[position + 1:]


def update(global_history, history, player):  # Author: Mikita Zyhmantovich
    cnt = 0
    for step in history:
        state, move = step
        if cnt % 2 == 0 and player == 'X' or cnt % 2 != 0 and player == 'O':
            global_history[state][move] += 3
        elif player == '/':
            global_history[state][move] += 1
        cnt += 1


def train(global_history):  # Author: Mikita Zyhmantovich
    NUM_GUMDROPS = 3
    state = initialise_board()
    history = []
    while not is_final(state):
        # Code that implements removed symmetry feature
        # symmetries = [state] + find_symmetries(state)
        # in_history = False
        # for symmetry in symmetries:
        #     if symmetry in global_history.keys():
        #         in_history = True
        #         global_history[state] = global_history[symmetry]
        #         break
        # if not in_history:
        if state not in global_history.keys():
            global_history[state] = [NUM_GUMDROPS for _ in state if _ == '_']
        move = choose(global_history[state])
        history.append((state, move))
        state = place(state, find_empty_index(state, move))
    if win_check(state, 'X'):
        update(global_history, history, 'X')
    elif win_check(state, 'O'):
        update(global_history, history, 'O')
    else:
        update(global_history, history, '/')


def choose(weights):  # Author: Mikita Zyhmantovich
    total = sum(weights)
    roll = random.randint(1, total + 1)
    for i in range(len(weights)):
        if roll <= weights[i]:
            return i
        roll -= weights[i]
    return 0


def choose_highest_value(weights): # Author: Andrei Nikiforov
    max_weight = max(weights)
    best_moves = [i for i in range(len(weights)) if weights[i] == max_weight]
    return random.choice(best_moves)


def find_empty_index(board, index): # Author: Andrei Nikiforov
    empty_indices = []

    for i in range(len(board)):
        if board[i] == '_':
            empty_indices.append(i)

    return empty_indices[index]


def initialise_board():
    return '_________'


def print_board(state):  # Author: Mikita Zyhmantovich
    print("|", end="")
    cnt = 1
    for char in state:
        print(char, end="|")
        if cnt % 3 == 0 and cnt < len(state) - 1:
            print("\n|", end="")
        cnt += 1


def play(model): # Author: Mikita Zyhmantovich
    state = "_________"
    while not is_final(state):
        print_board(state)
        i = int(input("\nchoose index: "))
        state = place(state, i)
        if state in model:
            state = place(state, find_empty_index(state, choose_highest_value(model[state])))
        else:
            continue
    print_board(state)
    print()
    if win_check(state, 'X'):
        print("Player X won")
    elif win_check(state, 'O'):
        print("Player O won")
    else:
        print("It's a draw")


menace = {}
for _ in range(20000):
    train(menace)

print(menace)
play(menace)
