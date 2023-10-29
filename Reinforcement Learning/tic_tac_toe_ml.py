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


def place(board, player, position):
    return board[:position] + player + board[position + 1:]


def choose(weights):
    total = sum(weights)
    roll = random.randint(1, total + 1)
    for i in range(len(weights)):
        if roll <= weights[i]:
            return i
        roll -= weights[i]


def initialise_board():
    return '_________'

