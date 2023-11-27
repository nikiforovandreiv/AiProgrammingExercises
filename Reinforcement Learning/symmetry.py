def find_symm(menace_dict, board, symm_dict):
    """
        Generally we have 7 symmetries of any board. These are symmetry by vertical axis, horizontal
        and diagonals. There are also 3 rotational symmetries. When we encounter a board, we want to
        find, which type of symmetry compared to the base version is it and store the formula for
        transforming the coordinates according to it.

        We return two values, the new board, and the type of symmetry needed to transform the board back
    """
    return_array = [None, None]

    # 90 deg
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["rotation_90"]])
        if new_board in menace_dict:
            return_array = [new_board, "rotation_270"]

    # 180 deg
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["rotation_180"]])
        if new_board in menace_dict:
            return_array = [new_board, "rotation_180"]

    # 270 deg
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["rotation_270"]])
        if new_board in menace_dict:
            return_array = [new_board, "rotation_90"]

    # vertical
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["vertical"]])
        if new_board in menace_dict:
            return_array = [new_board, "vertical"]

    # horizontal
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["horizontal"]])
        if new_board in menace_dict:
            return_array = [new_board, "horizontal"]

    # main diagonal
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["diagonal_main"]])
        if new_board in menace_dict:
            return_array = [new_board, "diagonal_main"]

    # sub diagonal
    if not return_array:
        new_board = ''.join([str(board[x - 1]) for x in symm_dict["diagonal_sub"]])
        if new_board in menace_dict:
            return_array = [new_board, "diagonal_sub"]

    return return_array


def revert_symm(move, board, symm_type, symm_dict):
    new_board = ''.join([str(board[x - 1]) for x in symm_dict[symm_type]])

    new_move = symm_dict[symm_type].index(move) + 1
    return new_board, new_move
