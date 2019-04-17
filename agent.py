#!/usr/bin/python3
# Have used start code from by Zac Partrige
# Step 1: Setting up the board object
# Step 2: Trying a pure Monte Carlo Search
# Step 3: Trying MiniMax
# Step 4: Trying MiniMax with Alpha Beta pruning
# Step 5: Trying Monte Carlo Tree Search


import socket
import sys

from ttt_board import TTTBoard
from agent_mcts import *
from agent_minimax import *
# from multiprocessing.dummy import Pool as ThreadPool

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# start game
GAME_BOARD = TTTBoard()


def play():
    """ takes an agent and finds the returns the best move """
    # we use minimax with alpha beta pruning initially a heuristic to get as many
    # 2 in a row/column/diagonals as possible.
    if GAME_BOARD.get_turn_counter() < 20:
        print("minimax agent used")
        move = agent_minimax(GAME_BOARD)
    else:
        print("MCTS agent used")
        move = agent_mcts(GAME_BOARD, time_limit=3)

    print("my move: board", GAME_BOARD.get_curr_board(), ", position", str(move))
    GAME_BOARD.place_move(move)
    print(GAME_BOARD)
    return move


# read what the server sent us and
# only parses the strings that are necessary
def display_turn(board):
    print("*" * 10 + " move: " + str(board.get_turn_counter()) + ", PLAYER " + str(board.get_players_turn()),
          " nodes explored: ", "*" * 10)


def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
    if command == "second_move":
        display_turn(GAME_BOARD)
        GAME_BOARD.place_move(int(args[1]), int(args[0]), 2)
        print(GAME_BOARD)
        display_turn(GAME_BOARD)
        return play()
    elif command == "third_move":
        # place_move the move that was generated for us
        display_turn(GAME_BOARD)
        GAME_BOARD.place_move(int(args[1]), int(args[0]), 1)
        print(GAME_BOARD)
        # place_move computer's last move
        display_turn(GAME_BOARD)
        GAME_BOARD.place_move(int(args[2]), GAME_BOARD.get_curr_board(), 2)
        print(GAME_BOARD)
        display_turn(GAME_BOARD)
        return play()
    elif command == "next_move":
        # opponents move
        display_turn(GAME_BOARD)
        print("opponents move: board -", GAME_BOARD.get_curr_board(), "position:", str(int(args[0])))
        GAME_BOARD.place_move(int(args[0]), GAME_BOARD.get_curr_board(), 2) # place_move opponents move
        print(GAME_BOARD)
        display_turn(GAME_BOARD)
        return play()
    elif command == "win":
        print("Yay!! We win!! 🏆")
        print(GAME_BOARD)
        return -1
    elif command == "loss":
        print("😫 We lost")
        print(GAME_BOARD)
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
