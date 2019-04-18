#!/usr/bin/python3
# Have used start code from by Zac Partrige

# Briefly describe how your program works, including any algorithms and data structures
# employed, and explain any design decisions you made along the way.

# Overall structure
# agent.py - contains the socket interface and calls agents to play Tic Tac Toe
#   there is a basic printout to facilitate debuggin and to see what is happening
# agent_X.py - contains the agents called by agent.py

# Step 1: Setting up the tic tac toe board object
# ttt_board.py contains the tic tac toe class. The game boards are represented as an
# object to allow for greater modularity, readability and greater ease in implementing
# the various algorithms. In particular, the most important class methods are the
# TTTBoard.get_child_boards() method which returns the child nodes (important in the
# search algorithms implemented), TTTBoard.get_winner() method which allows the search
# algorithms to know if terminal node has been reached. The board was represented as a
# numpy list to facilitate faster read times. (creation?)

# Step 2: Trying a pure Monte Carlo Search
# To avoid having to create a heuristic/evaluation function, my first attempt was to try
# simple pure Monte Carlo Search, simulating games until  a terminal state is reached by
# randomising each players moves. This agent did not perform very well, and was beaten
# by lookt at a search depth of 2+ almost all the time. As the game progresses, the
# effective branching factor declines and the average number of moves needed to be
# simulated until a terminal state is reached declines. As such I attempted increases the
# number of simulations according the the number of turns on the game board (stored in the
# game board object). This still did not help too much.

# Step 3: Trying MiniMax
# I next implemented a MiniMax search (using a random move as a heuristic for now). I
# could only achieve search depths of 3 towards the beginning of the game and it did not
# perform too much better than the pure Monte Carlo search. Again, even experimenting with
# increasing the search depth as the game progresses did not help too much.

# Step 4: Trying MiniMax with Alpha Beta pruning
# I next added alpha beta pruning to avoid wastefully searching nodes. I was able to
# increase the search depth to 4 towards the beginning of the game without timing out. The
# MiniMax search with Alpha Beta pruning was performing better than the MiniMax and the
# pure Monte Carlo search, even with a random heuristic/evaluation function.

# Step 5: Refining Heuristics
# Several heuristics for the MiniMax searhes were tried. I tried heuristics that would
# favour pieces in the centre (position 5) and corners (positions 1, 3, 7, 9), the logic
# being that it would open up more attack opportunities whilst denying the opponent the
# same opportunities. This helped the MiniMax algorithm somewhat. The heuristic which
# the most value was one which favoured nodes that the most "almost wins" (2 in a row,
# column, or diagonal) that was not blocked by the opponent. Implementing this heuristic
# allowed my agent to beat the lookt agent at a depth of 2 perhaps 60% of the time.

# Step 6: Trying Monte Carlo Tree Search
#

# Future development ideas
# At this stage what is holding back my agent is the efficiency of the code. I am only
# able to MiniMax search at a depth of 4 initially, and ~6 after 30 moves. Some
# profiling should be done to see where the bottlenecks are. Python was chosen for its
# readibility and ease of programming, but perhaps after I make my algorithms and data
# structures more efficient, I could consider implementing in say C.


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
    if GAME_BOARD.get_turn_counter() < 5:
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
