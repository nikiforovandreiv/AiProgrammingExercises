"""
Author: Sergei Baginskii

Version of MENACE with symmetry checking

For now, the model more or less works.
However, it often makes moves that makes no sense whatsoever
"""

import random
import supervisor
import symmetry


class Menace:
    def __init__(self, supervise=False):
        self._menace_system = {}
        self.supervise = supervise
        # parameter supervise enables bot, that makes "good" moves for menace to study better
        # dictionary containing all possible symmetries of a board. It has the following syntax:
        # numbers in the arrays in the dictionary represent in which places will the elements from old board
        # now be staying (i.e. in rotation for 90 degrees CLOCKWISE first element will be on the third place).
        # The elements are numbered from left to right from top to bottom
        self._symm_dict = {
            "rotation_90": [7, 4, 1, 8, 5, 2, 9, 6, 3],
            "rotation_180": [9, 8, 7, 6, 5, 4, 3, 2, 1],
            "rotation_270": [3, 6, 9, 2, 5, 8, 1, 4, 7],
            "vertical": [3, 2, 1, 6, 5, 4, 9, 8, 7],
            "horizontal": [7, 8, 9, 4, 5, 6, 1, 2, 3],
            "diagonal_main": [1, 4, 7, 2, 5, 8, 3, 6, 9],
            "diagonal_sub": [9, 6, 3, 8, 5, 2, 7, 4, 1]
        }

    def play_game(self):
        symmetry_type = ""
        menace_turn = "O"
        supervisor_turn = "X"
        board = "_________"
        history = []  # stores tuples of (board, move)
        # cycle goes until game is over
        while self.game_over(board) == "?":
            if self.supervise:
                # supervisor makes a move
                supervisor_move = supervisor.supervise(board, supervisor_turn)
                board = self.make_move(board, supervisor_move)
            if board not in self._menace_system:
                new_board, symmetry_type = symmetry.find_symm(self._menace_system, board, self._symm_dict)

                # symmetry was found
                if new_board is not None:
                    board = new_board

                # symmetry wasn't found
                else:
                    self._menace_system[board] = [0] * 9
                    for i, elem in enumerate(board):
                        if elem == "_":
                            self._menace_system[board][i] = 3

            # stores moves in the format [n, i, m, n, k, i, ...], where numbers represent index of a move in a string
            # i.e. move in the left top square would be numbered 0, move in the center would be numbered 4.
            # note, that we can store multiple instances of the same number, this increases the chances of successful
            # moves to be chosen
            possible_moves = []

            for i, elem in enumerate(self._menace_system[board]):
                if elem > 0:
                    for _ in range(elem):
                        possible_moves.append(i)

            # if the list of moves in the menace was empty due to unfortunate sequence of games we
            # just add all the possible moves to the pool.
            if not possible_moves:
                for i, elem in enumerate(board):
                    if elem == "_":
                        possible_moves.append(i)

            move = random.choice(possible_moves)

            # if we originally discovered the board as a symmetry, we should convert back
            if symmetry_type:
                board, move = symmetry.revert_symm(move, board, symmetry_type, self._symm_dict)

            history.append((board, move))
            board = self.make_move(board, move)

        winner = self.game_over(board)
        self.update_menace(history, winner)

    def make_move(self, board, move):
        move_count = 0
        # to determine who is making a move now
        for elem in board:
            if elem == "_":
                move_count += 1

        if move_count % 2 == 1:
            board_new = board[:move] + "X" + board[move + 1:]
        else:
            board_new = board[:move] + "O" + board[move + 1:]

        return board_new

    def game_over(self, board):
        """
        :param board:
        :return: / = draw, X = crosses, O = circles, ? - no winner
        """
        # Rows and Columns
        for player in ["X", "O"]:
            for i in range(3):
                # Rows
                if all(board[i * 3 + j] == player for j in range(3)):
                    return player
                # Columns
                if all(board[j * 3 + i] == player for j in range(3)):
                    return player

            # Top-Left to Bottom-Right Diagonals
            if all(board[i * 3 + i] == player for i in range(3)):
                return player
            # Bottom-Left to Top-Right Diagonals
            if all(board[i * 3 + 2 - i] == player for i in range(3)):
                return player
            # If there is no winner yet, the position is either not final or a draw
            for char in board:  # Check if it's final
                if char == '_':
                    return "?"
            return "/"

    def update_menace(self, history, winner, menace_turn="O"):
        """
        System learns based on the previous game.
        Indexation in updating system means that we increase or decrease the number of "gumdrops" in the
        corresponding turn possibility pool.
        """
        for i, event in enumerate(history):
            if i % 2 == 0:
                if winner == "X":
                    self._menace_system[event[0]][event[1]] += 1
                if winner == "O":
                    self._menace_system[event[0]][event[1]] -= 1
            if i % 2 == 1:
                if winner == "X":
                    self._menace_system[event[0]][event[1]] -= 1
                if winner == "O":
                    self._menace_system[event[0]][event[1]] += 1

    def __str__(self):
        """Magic method used in debugging"""
        return f"There are {len(self._menace_system)} variants in the system"

    def print_board(self, state):
        print("|", end="")
        cnt = 1
        for char in state:
            print(char, end="|")
            if cnt % 3 == 0 and cnt < len(state) - 1:
                print("\n|", end="")
            cnt += 1
        print()

    def menace_vs_player(self):
        symmetry_type = ""

        board = "_________"
        self.print_board("123456789")
        turn = 1

        # for now, it assumes you make only correct turns and if the game ends in a draw it says player won
        while self.game_over(board) == "?":
            # player's turn
            turn = int(input("Make a turn: \n"))
            board = self.make_move(board, turn - 1)
            if self.game_over(board) != "?":
                break

            # menace's turn
            possible_moves = []
            if board not in self._menace_system:
                new_board, symmetry_type = symmetry.find_symm(self._menace_system, board, self._symm_dict)

                # symmetry was found
                if new_board is not None:
                    board = new_board

                # symmetry wasn't found, just add all possible turns
                else:
                    for i, elem in enumerate(board):
                        if elem == "_":
                            possible_moves.append(i)

            # if we didn't already fill the possible moves with all the possibilities
            if not possible_moves:
                for i, elem in enumerate(self._menace_system[board]):
                    if elem > 0:
                        for _ in range(elem):
                            possible_moves.append(i)

                # if the list of moves in the menace was empty due to unfortunate sequence of games we
                # just add all the possible moves to the pool.
                if not possible_moves:
                    for i, elem in enumerate(board):
                        if elem == "_":
                            possible_moves.append(i)

            move = random.choice(possible_moves)

            # if we originally discovered the board as a symmetry, we should convert back
            if symmetry_type:
                board, move = symmetry.revert_symm(move, board, symmetry_type, self._symm_dict)

            board = self.make_move(board, move)
            self.print_board(board)
        if self.game_over(board) == "X":
            print("Player X won")
        elif self.game_over(board) == "O":
            print("Player O won")
        else:
            print("It's a draw")


if __name__ == "__main__":

    menace = Menace()
    for _ in range(10000):
        menace.play_game()

    print(menace)

    menace.menace_vs_player()
