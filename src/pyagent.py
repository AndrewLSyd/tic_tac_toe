#!/usr/bin/python3
# Sample starter bot by Zac Partrige
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np
import random
# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
current_board = 0  # this is the current board to play in

# print a row
# This is just ported from game.c
def print_board_row(a, b, c, i, j, k):
    print("", boards[a][i], boards[a][j], boards[a][k], end=" | ")
    print(boards[b][i], boards[b][j], boards[b][k], end=" | ")
    print(boards[c][i], boards[c][j], boards[c][k])

# Print the entire board
# This is just ported from game.c
def print_board():
    print_board_row(1, 2, 3, 1, 2, 3)
    print_board_row(1, 2, 3, 4, 5, 6)
    print_board_row(1, 2, 3, 7, 8, 9)
    print(" ------+-------+------")
    print_board_row(4, 5, 6, 1, 2, 3)
    print_board_row(4, 5, 6, 4, 5, 6)
    print_board_row(4, 5, 6, 7, 8, 9)
    print(" ------+-------+------")
    print_board_row(7, 8, 9, 1, 2, 3)
    print_board_row(7, 8, 9, 4, 5, 6)
    print_board_row(7, 8, 9, 7, 8, 9)
    print()


# converting to a board class
class TTTBoard:
    """
    ultimate tic tac toe board object
    """
    def __init__(self):
        self._board = np.zeros((10, 10), dtype="int8")
        # this is the current board to play in
        self._current_board = 0

    def print_board_row(self, a, b, c, i, j, k):
        out1 = " " + str(self._board[a][i]) + " " + str(self._board[a][j]) + " " + str(self._board[a][k]) + " | "
        out2 = str(self._board[b][i]) + " " + str(self._board[b][j]) + " " + str(self._board[b][k]) + " | "
        out3 = str(self._board[c][i]) + " " + str(self._board[c][j]) + " " + str(self._board[c][k]) + " | "
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
        return self._current_board

    def place(self, board, num, player):
        """
        sets a piece on the board
        """
        self._current_board = num  # changes the current game board
        assert self._board[board][num] == 0  # check that place is empty
        self._board[board][num] = player

    def get_empty_pos(self):
        """
        returns tuple of empty positions from the current board
        """
        empty_positions = []
        for position in range(1, 10):
            if self._board[self._current_board, position] == 0:
                empty_positions.append(position)
        return empty_positions

    def get_rand_empty_pos(self):
        """
        returns random empty position from current board
        """
        return random.choice(self.get_empty_pos())


test_board = TTTBoard()
print(test_board)
test_board.place(1,1,1)
# test_board.place(1,1,1)
print(test_board)
print(test_board.get_empty_pos())
print(test_board.get_rand_empty_pos())


# start game
game_board = TTTBoard()

# choose a move to play
def play():

    move = game_board.get_rand_empty_pos()
    print("current board:", game_board.get_curr_board(), "legal moves:", game_board.get_empty_pos(), "agent move:", move)
    game_board.place(game_board._current_board, move, 1)

    return move

# place a move in the global boards
def place(board, num, player):
    global current_board
    current_board = num
    boards[board][num] = player

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
        print(game_board)
        game_board.place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        print("*" * 20 + "third move" + "*" * 20)
        # place the move that was generated for us
        game_board.place(int(args[0]), int(args[1]), 1)
        # place their last move
        game_board.place(current_board, int(args[2]), 2)
        return play()
    elif command == "next_move":
        # place opponents move
        game_board.place(current_board, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yey!! We win!! 🏆")
        print(game_board)
        return -1
    elif command == "loss":
        print("😫 We lost")
        print(game_board)
        return -1
    return 0

# connect to socket
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

        s.connect(('localhost', port))
        while True:
            text = s.recv(1024).decode()
            if not text:
                continue
            for line in text.split("\n"):
                response = parse(line)
                if response == -1:
                    return
                elif response > 0:
                    s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
