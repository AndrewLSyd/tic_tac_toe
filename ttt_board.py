import numpy as np
import random


class TTTBoard:
    """ ultimate tic tac toe board object """
    def __init__(self, board=None):
        # the boards are of size 10 because index 0 isn't used
        # if no board specified, then create one
        if board is None:
            self._board = np.zeros((10, 10), dtype="int8")
        else:
            self._board = board
        self._current_board = 5
        self._turn_counter = 0
        self._players_turn = 1
        self._prev_player = 2

    def print_board_row(self, a, b, c, i, j, k):
        """ prints a row of the board"""
        out1 = " " + str(self._board[a][i]) + " " + str(self._board[a][j]) +\
               " " + str(self._board[a][k]) + " | "
        out2 = str(self._board[b][i]) + " " + str(self._board[b][j]) + " " +\
               str(self._board[b][k]) + " | "
        out3 = str(self._board[c][i]) + " " + str(self._board[c][j]) + " " +\
               str(self._board[c][k]) + " | "
        return out1 + out2 + out3

    def __str__(self):
        output = self.print_board_row(1, 2, 3, 1, 2, 3) + "\n" + \
                 self.print_board_row(1, 2, 3, 4, 5, 6) + "\n" + \
                 self.print_board_row(1, 2, 3, 7, 8, 9) + "\n" + \
                 " ------+-------+------" + "\n" + \
                 self.print_board_row(4, 5, 6, 1, 2, 3) + "\n" + \
                 self.print_board_row(4, 5, 6, 4, 5, 6) + "\n" + \
                 self.print_board_row(4, 5, 6, 7, 8, 9) + "\n" + \
                 " ------+-------+------" + "\n" + \
                 self.print_board_row(7, 8, 9, 1, 2, 3) + "\n" + \
                 self.print_board_row(7, 8, 9, 4, 5, 6) + "\n" + \
                 self.print_board_row(7, 8, 9, 7, 8, 9) + "\n"
        return output

    def get_rows(self, board):
        """ input: [1, 9]
         returns a list of all the rows of a board"""
        return [self._board[board, 1:4], self._board[board, 4:7], self._board[board, 7:10]]

    def get_cols(self, board):
        """ input: [1, 9]
        returns a list of arrays all the cols of a board"""
        x = np.reshape(self._board[board, 1:10], [3, 3])
        return [x[:, 0], x[:, 1], x[:, 2]]

    def get_diags(self, board):
        """ input: [1, 9]
        returns a list of arrays of the two diagonals of a board"""
        return [np.array([self._board[board, 1], self._board[board, 5], self._board[board, 9]]),
                np.array([self._board[board, 3], self._board[board, 5], self._board[board, 7]])]

    def get_board_pos(self, board, position):
        """ input: [1, 9], [1, 9]
        returns the value stored at a board position """
        return self._board[board, position]

    def get_curr_board(self):
        """ gets the current sub board number [1, 9] """
        return self._current_board

    def get_turn_counter(self):
        """ returns the number of turns the board has had """
        return self._turn_counter

    def get_players_turn(self):
        """ returns current player (1 or 2) """
        return self._players_turn

    def get_prev_player(self):
        """ returns previous player """
        return self._prev_player

    def clone(self):
        """ return copy of the board """
        clone = TTTBoard(np.copy(self._board))
        clone._current_board = self._current_board
        clone._players_turn = self._players_turn
        clone._turn_counter = self._turn_counter
        clone._prev_player = self._prev_player
        return clone

    def place_move(self, num, board=None, player=None):
        """ sets a piece on the board, incrementing turn counter, changing current board
         and changing player turn. If no board of player is specified the correct
          values are used. The parameters are there for manual overiding. """
        if board is None:
            board = self._current_board
        if player is None:
            player = self._players_turn

        self._board[board][num] = player  # sets down piece
        self._current_board = num  # changes the current game board

        # change turn
        if player == 1:
            self._players_turn = 2
            self._prev_player = 1
        elif player == 2:
            self._players_turn = 1
            self._prev_player = 2

        self._turn_counter += 1  # increments turn counter

    def get_moves(self):
        """ returns list of empty positions from the current board """
        if self.get_winner():
            return []
        empty_positions = []
        for position in range(1, 10):
            if np.sum(self._board[self._current_board, position]) == 0:
                empty_positions.append(position)
        return empty_positions

    def get_rand_legal_move(self):
        """ returns random empty position from current board """
        legal_moves = self.get_moves()
        if legal_moves:  # if there is a legal move
            return random.choice(legal_moves)
        return None

    def place_rand_move(self):
        """ places a random legal move on the board """
        self.place_move(self.get_rand_legal_move())

    def rollout(self):
        """ plays random move until a terminal state (rollout) """
        while self.get_moves() != []:
            self.place_rand_move()

    def check_win_sub_board(self, board):
        """ returns the winner of a sub board (1 or 2) """
        # rows
        for row in range(3):
            if self._board[board, 1 + row * 3] == self._board[board, 2 + row * 3]\
                    == self._board[board, 3 + row * 3] > 0:
                return self._board[board, 1 + row * 3]
        # cols
        for col in range(3):
            if self._board[board, 1 + col] == self._board[board, 4 + col] == self._board[board, 7 + col] > 0:
                return self._board[board, 1 + col]
        # diag top left to bot right
        if self._board[board, 1] == self._board[board, 5] == self._board[board, 9] > 0:
            return self._board[board, 1]
        # diag top right to bot left
        if self._board[board, 3] == self._board[board, 5] == self._board[board, 7] > 0:
            return self._board[board, 3]
        return None

    def get_winner(self):
        """ checks all boards for a winner and returns 1 or 2 (the winner) """
        for sub_board in range(1, 10):
            sub_board_win = self.check_win_sub_board(sub_board)
            if sub_board_win:
                return self.check_win_sub_board(sub_board)
        return None

    def get_curr_players_result(self, player):
        if self.get_winner() == player:
            return 1.0
        if self.get_winner() is None:
            return 0.5
        return 0.0

    def get_child_boards(self):
        """ returns child boards. returns none if no moves """
        if self.get_winner():
            return None
        child_nodes = []
        for move in self.get_moves():
            board_clone = self.clone()  # make copy of board
            board_clone.place_move(move)  # place_move move from valid moves
            child_nodes.append(board_clone)  # add to list of nodes
        return child_nodes
