# Author: Mikita Zyhmantovich
import itertools
import random


def supervise(board, turn):
    try:
        # first we check if we can win
        move = find_win(board, turn)
        if move != -1:
            return move
        # if no wins we deflect threats
        opponent_turn = "O" if turn == "X" else "X"
        move = find_win(board, opponent_turn)
        if move != -1:
            return move
        # if nothing to deflect, place in the center
        if board[4] == '_':
            return 4

        # if not in center, place it in one of the corners
        potential_indexs = []
        for i in range(9):
            if i in [0, 2, 6, 8] and board[i] == "_":
                potential_indexs.append(i)
        if len(potential_indexs) != 0:
            return random.choice(potential_indexs)
        # otherwise, any possible move
        for i in range(9):
            if board[i] == "_":
                potential_indexs.append(i)
        if len(potential_indexs) != 0:
            return random.choice(potential_indexs)
        raise NotImplementedError
    except NotImplementedError:
        print("No right move")


def find_win(board, turn):
    """
    :param board:
    :param turn:
    :return: position of move that wins, otherwise -1
    """
    permutations = []
    # generate list with all possible strings that lack one symbol before being 3 in a row
    for seq in itertools.permutations(f"{turn}{turn}_"):
        permutations.append("".join(seq))
    for i in range(0, 9, 3):  # rows
        if board[i:i + 3] in permutations:  # find potential row
            for j, char in enumerate(board[i:i + 3]):  # find index of an empty position
                if char == "_":
                    return i + j
    for i in range(3):
        # we find potential column
        column = [board[j * 3 + i] for j in range(3)]
        column = "".join(column)
        if column in permutations:
            for j, char in enumerate(column):  # we find index of an empty position
                if char == "_":
                    return j * 3 + i
    # diagonals
    diagonal = ''.join([board[i * 3 + i] for i in range(3)])
    if diagonal in permutations:
        for i, char in enumerate(diagonal):  # we find index of an empty position
            if char == "_":
                return i * 3 + i

    diagonal = ''.join([board[i * 3 + 2 - i] for i in range(3)])
    if diagonal in permutations:
        for i, char in enumerate(diagonal):
            if char == "_":
                return i * 3 + 2 - i
    return -1
