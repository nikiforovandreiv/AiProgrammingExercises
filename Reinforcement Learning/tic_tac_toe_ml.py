# Placement information

# | _ | _ | _ |
# | _ | _ | _ | = '_________'
# | _ | _ | _ |

# PLacement index
# | 0 | 1 | 2 |
# | 3 | 4 | 5 | = '012345678'
# | 6 | 7 | 9 |

# | X | _ | O |
# | _ | X | _ | = 'X_O_X_O_X'
# | O | _ | X |

# | O | _ | O |
# | _ | X | _ | = 'O_O_X_X_X'
# | X | _ | X |

import random


def win_check(board, player):
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


def is_final(state):
    if not win_check(state, 'X') and not win_check(state, 'O'):  # if X didn't win as well as O and board is full then
        for char in state:                                       # it's a draw
            if char == '_':
                return False
    return True  # some player won, so the state is final


def place(board, position):
    if board.count('X') > board.count('O'):
        player = 'O'
    else:
        player = 'X'

    return board[:position] + player + board[position + 1:]


def update(global_history, history, player):
    cnt = 0
    for step in history:
        state, move = step
        if cnt % 2 == 0 and player == 'O' or cnt % 2 != 0 and player == 'X':
            global_history[state][move] += 3
        elif player == '/':
            global_history[state][move] += 1


def train(global_history):
    NUM_GUMDROPS = 1
    state = initialise_board()
    history = []
    while not is_final(state):
        if state not in global_history.keys():
            global_history[state] = [NUM_GUMDROPS for _ in state if _ == '_']
        move = choose(global_history[state])
        history.append((state, move))
        state = place(state, move)
    if win_check(state, 'X'):
        update(global_history, history, 'X')
    elif win_check(state, 'O'):
        update(global_history, history, 'O')


def choose(weights):
    total = sum(weights)
    roll = random.randint(1, total + 1)
    for i in range(len(weights)):
        if roll <= weights[i]:
            return i
        roll -= weights[i]


def choose_highest_value(weights):
    max_weight = max(weights)
    best_moves = [i for i in range(len(weights)) if weights[i] == max_weight]
    return random.choice(best_moves)

def initialise_board():
    return '_________'
