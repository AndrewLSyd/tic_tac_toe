#!/usr/bin/python3
# Sample starter bot by Zac Partrige
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np
import random
import math
# from multiprocessing.dummy import Pool as ThreadPool

N_TRIALS = 200
DEPTH_FACTOR = 0.8  # increase number of searches at every move by this factor
ILLEGAL_MOVE = -1_000_000_000  # arbitrarily low number to indicate illegal move

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here


# converting to a board class
class TTTBoard:
    """ ultimate tic tac toe board object """
    def __init__(self, board=None, current_board=0, players_turn=1, num_turns=0):
        # the boards are of size 10 because index 0 isn't used
        # if no board specified, then create one
        if board is None:
            self._board = np.zeros((10, 10), dtype="int8")
        else:
            self._board = board
        self._current_board = current_board
        self._num_turns = num_turns
        self._players_turn = players_turn

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
        """ gets the value stored at a board position [1, 9], [1, 9] """
        return self._board[board, position]

    def get_curr_board(self):
        """ gets the current sub board number [1, 9] """
        return self._current_board

    def get_num_turns(self):
        """ returns the number of turns the board has had """
        return self._num_turns

    def get_players_turn(self):
        """ returns current player (1 or 2) """
        return self._players_turn

    def clone(self):
        """ return copy of the board """
        return TTTBoard(np.copy(self._board), self._current_board, self._players_turn,
                        self.get_num_turns())

    def place(self, board, num, player=None):
        """ sets a piece on the board, incrementing turn counter, changing current board
         and changing player turn """
        if player is None:
            player = self._players_turn

        self._num_turns += 1
        self._current_board = num  # changes the current game board
        self._board[board][num] = player  # sets down piece
        # change turn
        if player == 1:
            self._players_turn = 2
        elif player == 2:
            self._players_turn = 1

    def get_legal_moves(self):
        """ returns list of empty positions from the current board """
        empty_positions = []
        for position in range(1, 10):
            if np.sum(self._board[self._current_board, position]) == 0:
                empty_positions.append(position)
        return empty_positions

    def get_rand_legal_move(self):
        """ returns random empty position from current board """
        empty_pos = self.get_legal_moves()
        if empty_pos:
            return random.choice(empty_pos)
        return None

    def check_win_sub_board(self, board):
        """ returns the winner of a sub board"""
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

    def check_win(self):
        """ checks all boards for a winner and returns 1 or 2 (the winner) """
        for sub_board in range(1, 10):
            sub_board_win = self.check_win_sub_board(sub_board)
            if sub_board_win:
                return self.check_win_sub_board(sub_board)
        return None

    def get_child_boards(self):
        """ returns child boards. returns none if no moves """
        if self.check_win():
            return None
        child_nodes = []
        for move in self.get_legal_moves():
            board_clone = self.clone()  # make copy of board
            board_clone.place(board_clone.get_curr_board(), move)  # place move from valid moves
            child_nodes.append(board_clone)  # add to list of nodes
        return child_nodes


def mc_trial(board, verbose=False):
    """
    This function takes a current board and plays out the board randomly until the end.'
    2 is returned if player 1 wins, -2 is returned if player 2 wins and 0 if there is
    a draw.
    """
    move = board.get_rand_legal_move()  # initial move
    outcome = None

    while not outcome and move:  # while there is no winner and there is a valid move
        board.place(board.get_curr_board(), move)
        move = board.get_rand_legal_move()  # get new move
        outcome = board.check_win()

    # scoring
    if outcome == 1:  # player wins
        score = 2
    elif outcome == 2:  # opponent wins
        score = -2
    else:
        score = 0  # draw

    if verbose:
        print(board)

    return score


def pure_MC(board, num_trials=N_TRIALS):
    """ returns the pure Monte Carlo value of a board """
    score = 0
    for _ in range(num_trials):
        board_clone = board.clone()
        score += mc_trial(board_clone)
    return score


 # | | | | ___ _   _ _ __(_)___| |_(_) ___ ___
 # | |_| |/ _ \ | | | '__| / __| __| |/ __/ __|
 # |  _  |  __/ |_| | |  | \__ \ |_| | (__\__ \
 # |_| |_|\___|\__,_|_|  |_|___/\__|_|\___|___/
def heur_pure_mc(board):
    """ pure Monte Carlo sim heuristic """
    if board.get_num_turns() < 20:  # to save computation, first few moves just pick random
        return random.randrange(-10, 11)
    return pure_MC(board, 2)


def heur_centre(board):
    """ heuristic based on number of pieces at position 5 """
    # 2/3s > middle > corners
    # count number of 1's
    total_in_centres = 0
    for sub_board in range(1, 10):
        value = board.get_board_pos(sub_board, 5)
        if value == 1:
            total_in_centres += 1
        elif value == 2:
            total_in_centres -= 1

    total_in_centre_board = 0
    # for position in range(1, 10):
    #     value = board.get_board_pos(5, position)
    #     if value == 1:
    #         total_in_centre_board += 1
    #     elif value == 2:
    #         total_in_centre_board -= 1

    return total_in_centres + total_in_centre_board


def heur_corners(board):
    """ heuristic based on number of pieces at the corners """
    total_in_corners = 0
    for sub_board in range(1, 10):
        for corner in [1, 3, 7, 9]:
            value = board.get_board_pos(sub_board, corner)
            if value == 1:
                total_in_corners += 1
            elif value == 2:
                total_in_corners -= 1

    return total_in_corners


def count_players_pieces(array, player):
    """ counts the number of player's pieces in an array
    e.g. a row, col or diag """
    count = 0
    for element in array:
        if element == player:
            count += 1
    return count


def heur_twos(board, full_output=False):
    """ heuristic which attempts to maximise number of twos
    counts number of boards with twos """
    twos_player = [0, 0]

    for player in [1, 2]:
        if player == 1:
            other_player = 2
        elif player == 2:
            other_player = 1
        for sub_board in range(1, 10):
            for row in board.get_rows(sub_board):
                if count_players_pieces(row, player) > 1 and count_players_pieces(row, other_player) == 0:
                    twos_player[player - 1] += 1
            for col in board.get_cols(sub_board):
                if count_players_pieces(col, player) > 1 and count_players_pieces(col, other_player) == 0:
                    twos_player[player - 1] += 1
            for diag in board.get_diags(sub_board):
                if count_players_pieces(diag, player) > 1 and count_players_pieces(diag, other_player) == 0:
                    twos_player[player - 1] += 1

    heuristic = twos_player[0] - twos_player[1]

    if full_output:
        return [twos_player, heuristic]
    return heuristic

def heur_my_strat(board):
    """ strategy that involves going for 2 in a row/col/diagonal whilst preferring
    centre pieces then corners """
    return 10 * heur_twos(board) + 2 * heur_centre(board) + heur_corners(board)

# choose a move to play
def final_heuristic(board, heuristic=heur_my_strat):
    """ returns heuristic estimate of position value from player 1s POV """
    if board.check_win() == 1:
        return 1_000_000 - board.get_num_turns()
    elif board.check_win() == 2:
        return -1_000_000 + board.get_num_turns()
    else:
        return heuristic(board)


def minimax(board, depth=3, verbose=False):
    """ minimax without ab pruning. can only seem to get depth 3 with this. """
    if board.check_win() or depth == 0:
        return final_heuristic(board)
    if board.get_players_turn() == 1:
        alpha = -float("inf")
        for child in board.get_child_boards():
            alpha = max(alpha, minimax(child, depth - 1))
        if verbose:
            print(board)
            print("ALPHA for depth", depth, "is", alpha)
        return alpha
    if board.get_players_turn() == 2:
        beta = float("inf")
        for child in board.get_child_boards():
            beta = min(beta, minimax(child, depth - 1))
        if verbose:
            print(board)
            print("BETA for depth", depth, "is", beta)
        return beta


def minimax_ab(board, alpha=-float("inf"), beta=float("inf"), depth=4):
    """ minimax WITH ab pruning. Can get at least depth 4 with pruning"""
    if board.check_win() or depth == 0:
        return final_heuristic(board)
    if board.get_players_turn() == 1:
        for child in board.get_child_boards():
            alpha = max(alpha, minimax_ab(child, alpha, beta, depth - 1))
            if alpha >= beta:
                return alpha
        return alpha
    if board.get_players_turn() == 2:
        for child in board.get_child_boards():
            beta = min(beta, minimax_ab(child, alpha, beta, depth - 1))
            if beta <= alpha:
                return beta
        return beta


# def play():
#     """ what this does"""
#     # move = game_board.get_rand_legal_move()
#     mc = pure_MC(game_board, N_TRIALS * math.ceil((1 + game_board.get_num_turns()) ** DEPTH_FACTOR))
#     move = mc[1]
#     print("number of sims:", str(math.ceil(N_TRIALS * (1 + game_board.get_num_turns()) ** DEPTH_FACTOR)))
#     print("top moves:", mc[0])
#     print("my move: board -", game_board.get_curr_board(), "position:", str(move))
#     game_board.place(game_board._current_board, move, 1)
#     print(game_board)
#     return move


def play(agent=minimax_ab):
    """ what this does """
    move_values = [ILLEGAL_MOVE] * 9  # illegal moves set to arbitrarily low number
    print('legal moves', game_board.get_legal_moves())
    # find value of all moves
    for move in game_board.get_legal_moves():
        board_clone = game_board.clone()
        board_clone.place(board_clone.get_curr_board(), move)
        if agent is minimax_ab:
            if game_board.get_num_turns() < 20:
                minimax_ab_depth = 4
            elif game_board.get_num_turns() < 35:
                minimax_ab_depth = 5
            elif game_board.get_num_turns() < 40:
                minimax_ab_depth = 6
            elif game_board.get_num_turns() < 45:
                minimax_ab_depth = 7
            else:
                minimax_ab_depth = 8
            # agent plays here and returns score of all moves
            move_values[move - 1] = agent(board_clone, depth=minimax_ab_depth)
        else:
            move_values[move - 1] = agent(board_clone)  # agent plays here and returns score of all moves
    print("move_values:", move_values)

    # get random max move
    best_move_value = -float("inf")
    best_moves_index = []

    for move_index in range(len(move_values)):
        # if we find a value as big as the current best move
        if move_values[move_index] == best_move_value:
            best_moves_index.append(move_index)
        elif move_values[move_index] > best_move_value:
            best_moves_index = [move_index]
            best_move_value = move_values[move_index]

    # choose a random best move
    move = random.choice(best_moves_index) + 1
    print("my move: board", game_board.get_curr_board(), ", position", str(move))
    game_board.place(game_board._current_board, move, 1)
    print(game_board)
    return move


# start game
game_board = TTTBoard()


# ********** SERVER STUFF BELOW **********
# read what the server sent us and
# only parses the strings that are necessary
def display_turn(board):
    print("*" * 20 + " move: " + str(board.get_num_turns()) + ", PLAYER " + str(board.get_players_turn()),
          "*" * 20)


def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
    if command == "second_move":
        display_turn(game_board)
        game_board.place(int(args[0]), int(args[1]), 2)
        print(game_board)
        display_turn(game_board)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        display_turn(game_board)
        game_board.place(int(args[0]), int(args[1]), 1)
        print(game_board)
        # place computer's last move
        display_turn(game_board)
        game_board.place(game_board.get_curr_board(), int(args[2]), 2)
        print(game_board)
        display_turn(game_board)
        return play()
    elif command == "next_move":
        # opponents move
        display_turn(game_board)
        print("opponents move: board -", game_board.get_curr_board(), "position:", str(int(args[0])))
        game_board.place(game_board.get_curr_board(), int(args[0]), 2) # place opponents move
        print(game_board)
        display_turn(game_board)
        return play()
    elif command == "win":
        print("Yay!! We win!! 🏆")
        print(game_board)
        return -1
    elif command == "loss":
        print("😫 We lost")
        print(game_board)
        return -1
    return 0


# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())


if __name__ == "__main__":
    main()
