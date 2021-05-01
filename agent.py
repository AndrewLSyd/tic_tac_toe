#!/usr/bin/python3
# Have used start code from by Zac Partrige

# Briefly describe how your program works, including any algorithms and data structures
# employed, and explain any design decisions you made along the way.
#
# *** Overall structure ***
# agent.py - contains the socket interface and calls agents to play Tic Tac Toe
#   there is a basic printout to facilitate debugging and to see what is happening
#   Play() function - this is what calls the agent. We can specify which agent to used,
#   under what parameters and at what turn here.
# agent_X.py - contains the agents called by agent.py
#
# *** Step 1: Setting up the tic tac toe board object ***
# ttt_board.py contains the tic tac toe class. The game boards are represented as an
# object to allow for greater modularity, readability and greater ease in implementing
# the various algorithms. In particular, the most important class methods are the
# TTTBoard.get_child_boards() method which returns the child nodes (important in the
# search algorithms implemented), TTTBoard.get_winner() method which allows the search
# algorithms to know if terminal node has been reached. The board was represented as a
# numpy list to facilitate faster read times. (creation?)
#
# *** Step 2: Trying a pure Monte Carlo Search ***
# To avoid having to create a heuristic/evaluation function, my first attempt was to try
# simple pure Monte Carlo Search, simulating games until  a terminal state is reached by
# randomising each players moves. This agent did not perform very well, and was beaten
# by lookt at a search depth of 2+ almost all the time. As the game progresses, the
# effective branching factor declines and the average number of moves needed to be
# simulated until a terminal state is reached declines. As such I attempted increases the
# number of simulations according the the number of turns on the game board (stored in the
# game board object). This still did not help too much.
#
# *** Step 3: Trying MiniMax ***
# I next implemented a MiniMax search (using a random move as a heuristic for now). I
# could only achieve search depths of 3 towards the beginning of the game and it did not
# perform too much better than the pure Monte Carlo search. Again, even experimenting with
# increasing the search depth as the game progresses did not help too much.
#
# *** Step 4: Trying MiniMax with Alpha Beta pruning ***
# I next added alpha beta pruning to avoid wastefully searching nodes. I was able to
# increase the search depth to 4 towards the beginning of the game without timing out. The
# MiniMax search with Alpha Beta pruning was performing better than the MiniMax and the
# pure Monte Carlo search, even with a random heuristic/evaluation function.
#
# *** Step 5: Refining Heuristics ***
# Several heuristics for the MiniMax searches were tried:
#
# ** Pure Monte Carlo Heuristic - heuristic.heur_pure_mc() **
# This proved to be not worth the computation required. It was not worth cutting the depth
# of my MiniMax search to use this heuristic).
#
# ** Position of pieces - heuristics.heur_corners() and heuristics.heur_centre() **
# This heuristic favours pieces in the centre (position 5) and corners (positions 1, 3, 7
# , 9), the logic being that it would open up more attack opportunities whilst denying the
# opponent the same opportunities. This helped the MiniMax algorithm somewhat.
#
#  ** Almost wins - heuristic.heur_twos() **
# The most effective heuristic I found was one that favoured "almost wins" (2 in a row,
# column, or diagonal) that was not blocked by the opponent. Implementing this heuristic
# allowed my agent to beat the lookt agent at a depth of 2 perhaps 60% of the time.
#
# Combinations of the above heuristics were also tried, but not found to be worth the
# extra computation time required.
#
# *** Step 6: Trying Monte Carlo Tree Search ***
# I am still not able to consistently beat the lookt opponent with a depth of greater than
# 3. My next attempt was to use a Monte Carlo Tree Search. This approach has a few
# advantages: we do not need a heuristic (it's not the easiest to come up with a heuristic
# for this game) and the algorithm can be stopped at anytime and the best estimate so far
# can be returned. This is useful for this assignment due to the "chess clock" time
# constraint of this assignment. This approach seemed to perform a little better than the
# MiniMax with alpha beta pruning. In the end, the agent I have adopted uses a MiniMax
# search with alpha beta pruning for the initial moves, trying to get as many "almost
# wins" (2 out of 3 in a row/column or diagonal) as a heuristic, before switching to a
# MCTS with a time limit.

# *** Future development ideas ***
# At this stage what is holding back my agent is the efficiency of the code. I am only
# able to MiniMax search at a depth of 4 initially, and ~6 after 30 moves. Some
# profiling should be done to see where the bottlenecks are. Python was chosen for its
# readability and ease of programming, but perhaps after I make my algorithms and data
# structures more efficient, I could consider implementing in a more low level language
# like C. If I had more time I would write code to simulate games to more objectively
# select algorithms and tune parameters. For example the exploration parameter in the
# MTCS could be tuned.


import socket
import sys

from ttt_board import TTTBoard  # importing my game board class
# importing game agents
from agent_mcts import agent_mcts
from agent_minimax import agent_minimax
from agent_pure_mc import agent_pure_mc

# from multiprocessing.dummy import Pool as ThreadPool

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# start game
GAME_BOARD = TTTBoard()


def play():
    """ takes an agent and finds the returns the best move """
    # we use Minimax with alpha beta pruning initially a heuristic to get as many
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
    """ displays a text summary of the turn """
    print("*" * 10 + " move: " + str(board.get_turn_counter()) + ", PLAYER "
          + str(board.get_players_turn()), " nodes explored: ", "*" * 10)


def parse(string):
    """ parses text received through the socket and plays the game """
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
    if command == "third_move":
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
    if command == "next_move":
        # opponents move
        display_turn(GAME_BOARD)
        print("opponents move: board -", GAME_BOARD.get_curr_board(), "position:",
              str(int(args[0])))
        # place_move opponents move
        GAME_BOARD.place_move(int(args[0]), GAME_BOARD.get_curr_board(), 2)
        print(GAME_BOARD)
        display_turn(GAME_BOARD)
        return play()
    if command == "win":
        print("Yay!! We win!! 🏆")
        print(GAME_BOARD)
        return -1
    if command == "loss":
        print("😫 We lost")
        print(GAME_BOARD)
        return -1
    return 0


def main():
    """ connection to socket """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    my_socket.connect(('localhost', port))
    while True:
        text = my_socket.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                my_socket.close()
                return
            if response > 0:
                my_socket.sendall((str(response) + "\n").encode())


if __name__ == "__main__":
    main()
