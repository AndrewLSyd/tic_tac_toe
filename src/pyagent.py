#!/usr/bin/python3
# Have used start code from by Zac Partrige
# Step 1: Setting up the board object
# Step 2: Trying a pure Monte Carlo Search
# Step 3: Trying MiniMax
# Step 4: Trying MiniMax with Alpha Beta pruning
# Step 5: Trying Monte Carlo Tree Search


import socket
import sys
import numpy as np
import random
from math import sqrt, log, ceil
import time
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
        self._turn_counter = num_turns
        self._players_turn = players_turn
        self.playerJustMoved = 2

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

    def get_num_turns(self):
        """ returns the number of turns the board has had """
        return self._turn_counter

    def get_players_turn(self):
        """ returns current player (1 or 2) """
        return self._players_turn

    def Clone(self):
        """ return copy of the board """
        clone = TTTBoard(np.copy(self._board), self._current_board, self._players_turn,
                        self.get_num_turns())
        clone.playerJustMoved = self.playerJustMoved
        return clone

    def DoMove(self, num, board=None, player=None):
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
            self.playerJustMoved = 1
        elif player == 2:
            self._players_turn = 1
            self.playerJustMoved = 2

        self._turn_counter += 1  # increments turn counter

    def GetMoves(self):
        """ returns list of empty positions from the current board """
        if self.check_win():
            return []
        empty_positions = []
        for position in range(1, 10):
            if np.sum(self._board[self._current_board, position]) == 0:
                empty_positions.append(position)
        return empty_positions

    def get_rand_legal_move(self):
        """ returns random empty position from current board """
        empty_pos = self.GetMoves()
        if empty_pos:
            return random.choice(empty_pos)
        return None

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

    def check_win(self):
        """ checks all boards for a winner and returns 1 or 2 (the winner) """
        for sub_board in range(1, 10):
            sub_board_win = self.check_win_sub_board(sub_board)
            if sub_board_win:
                return self.check_win_sub_board(sub_board)
        return None

    def GetResult(self, player):
        if self.check_win() == player:
            return 1.0
        if self.check_win() is None:
            return 0.5
        return 0.0


    def get_child_boards(self):
        """ returns child boards. returns none if no moves """
        if self.check_win():
            return None
        child_nodes = []
        for move in self.GetMoves():
            board_clone = self.Clone()  # make copy of board
            board_clone.DoMove(move)  # DoMove move from valid moves
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
        board.DoMove(move)
        move = board.get_rand_legal_move()  # get new move
        outcome = board.check_win()

    # scoring
    if outcome == 1:  # player wins
        score = 1
    elif outcome == 2:  # opponent wins
        score = -1
    else:
        score = 0  # draw
    if verbose:
        print(board)
    return score


def pure_MC(board, num_trials=N_TRIALS):
    """ returns the pure Monte Carlo value of a board """
    score = 0
    for _ in range(num_trials):
        board_clone = board.Clone()
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


def heur_twos(board):
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

    return heuristic


def heur_my_strat(board):
    """ strategy that involves going for 2 in a row/col/diagonal whilst preferring
    centre pieces then corners """
    return 10 * heur_twos(board) + 2 * heur_centre(board) + heur_corners(board)


# choose a move to play
def final_heuristic(board, heuristic=heur_twos):
    """ returns heuristic estimate of position value from player 1s POV """
    if board.check_win() == 1:
        return 1_000_000 - board.get_num_turns()
    elif board.check_win() == 2:
        return -1_000_000 + board.get_num_turns()
    else:
        return heuristic(board)

###########################################################################
#                              MINIMAX                                    #
###########################################################################

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


nodes_explored = 0

def minimax_ab(board, alpha=-float("inf"), beta=float("inf"), depth=4):
    """ minimax WITH ab pruning. Can get at least depth 4 with pruning"""
    global nodes_explored
    if board.check_win() or depth == 0:
        return final_heuristic(board)
    if board.get_players_turn() == 1:
        for child in board.get_child_boards():
            nodes_explored += 1
            alpha = max(alpha, minimax_ab(child, alpha, beta, depth - 1))
            # print("DEPTH:", depth, "ALPHA:", alpha)
            if alpha >= beta:
                return alpha
        return alpha
    if board.get_players_turn() == 2:
        for child in board.get_child_boards():
            nodes_explored += 1
            beta = min(beta, minimax_ab(child, alpha, beta, depth - 1))
            # print("DEPTH:", depth, "BETA:", beta)
            if beta <= alpha:
                return beta
        return beta


def play(agent=minimax_ab):
    """ takes an agent and finds the returns the best move """
    # global nodes_explored
    # nodes_explored = 0
    # move_values = [ILLEGAL_MOVE] * 9  # illegal moves set to arbitrarily low number
    # print('legal moves', game_board.GetMoves())
    # # find value of all moves
    # for move in game_board.GetMoves():
    #     board_clone = game_board.Clone()
    #     board_clone.DoMove(move)
    #     if agent is minimax_ab:
    #         if game_board.get_num_turns() < 20:
    #             minimax_ab_depth = 4
    #         elif game_board.get_num_turns() < 30:
    #             minimax_ab_depth = 4
    #         elif game_board.get_num_turns() < 35:
    #             minimax_ab_depth = 5
    #         elif game_board.get_num_turns() < 38:
    #             minimax_ab_depth = 6
    #         elif game_board.get_num_turns() < 40:
    #             minimax_ab_depth = 6
    #         else:
    #             minimax_ab_depth = 7
    #         # agent plays here and returns score of all moves
    #         move_values[move - 1] = agent(board_clone, depth=minimax_ab_depth)
    #     else:
    #         move_values[move - 1] = agent(board_clone)  # agent plays here and returns score of all moves
    # print("move_values:", move_values)
    #
    # # get random max move
    # best_move_value = -float("inf")
    # best_moves_index = []
    #
    # for move_index in range(len(move_values)):
    #     # if we find a value as big as the current best move
    #     if move_values[move_index] == best_move_value:
    #         best_moves_index.append(move_index)
    #     elif move_values[move_index] > best_move_value:
    #         best_moves_index = [move_index]
    #         best_move_value = move_values[move_index]
    #
    # # choose a random best move
    # move = random.choice(best_moves_index) + 1
    # print("my move: board", game_board.get_curr_board(), ", position", str(move))
    # game_board.DoMove(move, player=1)
    # print(game_board)
    # return move
    iterations = ceil(750 * (1 + 0.02) ** game_board.get_num_turns())
    # if game_board.get_num_turns() < 20:
    #     iterations = 750
    # elif game_board.get_num_turns() < 30:
    #     iterations = 1000
    # elif game_board.get_num_turns() < 35:
    #     iterations = 1500
    # elif game_board.get_num_turns() < 38:
    #     iterations = 1750
    # elif game_board.get_num_turns() < 40:
    #     iterations = 2000
    # else:
    #     iterations = 2500
    move = UCT(rootstate=game_board, itermax=iterations, verbose=False)
    print("my move: board", game_board.get_curr_board(), ", position", str(move))
    game_board.DoMove(move, player=1)
    print(game_board)
    return move


###########################################################################
#                       MONTE CARLO TREE SEARCH                           #
###########################################################################
class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(
                node.playerJustMoved))  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if verbose:
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


# start game
game_board = TTTBoard()


# ********** SERVER STUFF BELOW **********
# read what the server sent us and
# only parses the strings that are necessary
def display_turn(board):
    print("*" * 20 + " move: " + str(board.get_num_turns()) + ", PLAYER " + str(board.get_players_turn()),
          " nodes explored: ", nodes_explored, "*" * 20)


def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
    if command == "second_move":
        display_turn(game_board)
        game_board.DoMove(int(args[1]), int(args[0]), 2)
        print(game_board)
        display_turn(game_board)
        return play()
    elif command == "third_move":
        # DoMove the move that was generated for us
        display_turn(game_board)
        game_board.DoMove(int(args[1]), int(args[0]), 1)
        print(game_board)
        # DoMove computer's last move
        display_turn(game_board)
        game_board.DoMove(int(args[2]), game_board.get_curr_board(), 2)
        print(game_board)
        display_turn(game_board)
        return play()
    elif command == "next_move":
        # opponents move
        display_turn(game_board)
        print("opponents move: board -", game_board.get_curr_board(), "position:", str(int(args[0])))
        game_board.DoMove(int(args[0]), game_board.get_curr_board(), 2) # DoMove opponents move
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
