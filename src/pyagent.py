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

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here


# converting to a board class
class TTTBoard:
    """ ultimate tic tac toe board object """
    def __init__(self, board=None, current_board=0, players_turn=1):
        # the boards are of size 10 because index 0 isn't used
        # if no board specified, then create one
        if board is None:
            self._board = np.zeros((10, 10), dtype="int8")
        else:
            self._board = board
        self._current_board = current_board
        self._num_turns = 0
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
        return TTTBoard(np.copy(self._board), self._current_board, self._players_turn)

    def place(self, board, num, player=None):
        """ sets a piece on the board """
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

    def get_empty_pos(self):
        """ returns list of empty positions from the current board """
        empty_positions = []
        for position in range(1, 10):
            if np.sum(self._board[self._current_board, position]) == 0:
                empty_positions.append(position)
        return empty_positions

    def get_rand_empty_pos(self):
        """ returns random empty position from current board """
        empty_pos = self.get_empty_pos()
        if empty_pos:
            return random.choice(empty_pos)
        return None

    def check_win_sub_board(self, board):
        """ returns the winner of a sub board"""
        # rows
        for row in range(3):
            if self._board[board, 1 + row * 3] == self._board[board, 2 + row * 3] == self._board[board, 3 + row * 3] > 0:
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

    def get_child_boards(self):
        """ returns child boards """
        if self.check_win():
            return None
        child_nodes = []
        for move in self.get_empty_pos():
            board_clone = self.clone()  # make copy of board
            board_clone.place(board_clone.get_curr_board(), move)  # place move from valid moves
            child_nodes.append(board_clone)  # add to list of nodes
        return child_nodes



def mc_trial(board, verbose=False):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player by
    making random moves, alternating between players. The function
    should return when the game is over.
    """
    player = 1  # if we are doing MC trial, then it is our turn to begin with
    initial_move = board.get_rand_empty_pos()  # initial move
    move = initial_move
    outcome = None

    while not outcome:
        if board.get_rand_empty_pos is []:  # if no more moves then draw
            break
        board.place(board.get_curr_board(), move, player)
        move = board.get_rand_empty_pos()
        # switch player
        if player == 1:
            player = 2
        else:
            player = 1
        outcome = board.check_win()
        # if verbose:
        #     print(board)

    # scoring
    if outcome == 1: # player wins
        score = 2
    elif outcome == 2:  # opponent wins
        score = -2
    else:
        score = 0  # draw

    if verbose:
        print(board)

    return score, initial_move


def mc_update_score(board, num_trials, verbose=False):
    # score_board = np.zeros(9, dtype="int8")
    # pool = ThreadPool(4)
    # results = pool.map(my_function, my_array)
    score_board = [-float("inf")] * 9
    for empty_pos in board.get_empty_pos():
        score_board[empty_pos - 1] = 0
    for n in range(num_trials):
        if verbose:
            print("*** trial", n, "***")
        new_board = board.clone()
        trial = mc_trial(new_board, verbose)
        score_board[trial[1] - 1] += trial[0]
        if verbose:
            print("winner:", trial[0])
    best_move = score_board.index(max(score_board))
    return score_board, best_move + 1


# choose a move to play
def heuristic(board):
    """ returns out_heur estimate of position value from player 1s POV """
    print("out_heur check win")
    print(board)
    if board.check_win() == 1:
        print("player 1 wins")
        return 1_000_000
    elif board.check_win() == 2:
        print("player 2 wins")
        return -1_000_000
    else:
        out_heur = random.randrange(-100, 101)
        print("out_heur estimate", out_heur)
        return out_heur


def minimax(board, depth):
    """ minimax without ab pruning """
    print("DEPTH:", depth)
    if board.check_win() or depth == 0:
        return heuristic(board)
    if board.get_players_turn() == 1:
        alpha = -float("inf")
        for child in board.get_child_boards():
            alpha = max(alpha, minimax(child, depth - 1))
        print("ALPHA for depth", depth, "is", alpha)
        print(board)
        return alpha
    if board.get_players_turn() == 2:
        beta = float("inf")
        for child in board.get_child_boards():
            beta = min(beta, minimax(child, depth - 1))
        print("BETA for depth", depth, "is", beta)
        print(board)
        return beta



# def play():
#     """ what this does"""
#     # move = game_board.get_rand_empty_pos()
#     mc = mc_update_score(game_board, N_TRIALS * math.ceil((1 + game_board.get_num_turns()) ** DEPTH_FACTOR))
#     move = mc[1]
#     print("number of sims:", str(math.ceil(N_TRIALS * (1 + game_board.get_num_turns()) ** DEPTH_FACTOR)))
#     print("top moves:", mc[0])
#     print("my move: board -", game_board.get_curr_board(), "position:", str(move))
#     game_board.place(game_board._current_board, move, 1)
#     print(game_board)
#     return move


def play():
    """ what this does"""
    scores = [-999_999_999] * 9
    print('empty_pos', game_board.get_empty_pos())
    for move in game_board.get_empty_pos():
        board_clone = game_board.clone()
        board_clone.place(board_clone.get_curr_board(), move)
        scores[move - 1] = minimax(board_clone, 3)
    print("scores:", scores)
    move = scores.index(max(scores)) + 1
    print("my move: board -", game_board.get_curr_board(), "position:", str(move))
    game_board.place(game_board._current_board, move, 1)
    print(game_board)
    return move


# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        # print(string)
        # print(string.split("("))
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        print("*" * 20 + "second move" + "*" * 20)
        game_board.place(int(args[0]), int(args[1]), 2)
        print(game_board)
        return play()
    elif command == "third_move":
        print("*" * 20 + "third move" + "*" * 20)
        # place the move that was generated for us
        game_board.place(int(args[0]), int(args[1]), 1)
        # place their last move
        game_board.place(game_board.get_curr_board(), int(args[2]), 2)
        print(game_board)
        return play()
    elif command == "next_move":
        # opponents move
        print("*" * 20 + " move: " + str(game_board.get_num_turns()) + ", OPPONENT " + "*" * 20)
        print("opponents move: board -", game_board.get_curr_board(), "position:", str(int(args[0])))
        game_board.place(game_board.get_curr_board(), int(args[0]), 2) # place opponents move
        print(game_board)
        print("*" * 20 + " move: " + str(game_board.get_num_turns()) + ", ME " + "*" * 20)
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


# start game
game_board = TTTBoard()


if __name__ == "__main__":
    main()
