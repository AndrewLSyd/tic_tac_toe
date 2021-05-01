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
        clone = TTTBoard(self._board.copy(self._board))
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

"""
Minimax agent with alpha beta pruning
"""
import random



ILLEGAL_MOVE = -1000000000  # arbitrarily low number to indicate illegal move


def minimax(board, depth=3, verbose=False):
    """ minimax without ab pruning. can only seem to get depth 3 with this. """
    if board.get_winner() or depth == 0:
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
    if board.get_winner() or depth == 0:
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


def agent_minimax(board):
    """ agent that applies minimax with AB pruning.
    input board state
    returns best move for player 1 """
    move_values = [ILLEGAL_MOVE] * 9  # illegal moves set to arbitrarily low number
    for move in board.get_moves():
        board_clone = board.clone()
        board_clone.place_move(move)
        if board.get_turn_counter() < 20:
            minimax_ab_depth = 4
        elif board.get_turn_counter() < 30:
            minimax_ab_depth = 4
        elif board.get_turn_counter() < 35:
            minimax_ab_depth = 5
        elif board.get_turn_counter() < 38:
            minimax_ab_depth = 6
        elif board.get_turn_counter() < 40:
            minimax_ab_depth = 6
        else:
            minimax_ab_depth = 7
        # agent plays here and returns score of all moves
        move_values[move - 1] = minimax_ab(board_clone, depth=minimax_ab_depth)
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

    return move
"""
Tic Tac Toe agent that uses a Monte Carlo Tree Search
"""
import time
import random
import math


class MCTSNode:
    """ Class for Node in the Monte Carlo Tree Search """
    def __init__(self, move=None, parent=None, state=None):
        # move that got us here
        self._move = move
        # parent node
        self._parent = parent
        self._children = []
        self._wins = 0  # number of wins
        self._visits = 0  # number of visits to this node
        # nodes not visited
        self._moves_not_tried = state.get_moves()
        self._prev_player = state.get_prev_player()

    def __repr__(self):
        out = "{Move - " + str(self._move) + " Wins/Visits:" + str(self._wins) + "/"\
                + str(self._visits) + " UCT:" + str(self._moves_not_tried) + "}"
        return out

    def get_wins(self):
        """ returns number of wins """
        return self._wins

    def get_visits(self):
        """ returns number of visits """
        return self._visits

    def get_move(self):
        """ returns move """
        return self._move

    def get_moves_not_tried(self):
        """ returns moves not tried """
        return self._moves_not_tried

    def get_parent(self):
        """ returns parent node """
        return self._parent

    def get_children(self):
        """ returns child nodes """
        return self._children

    def get_prev_player(self):
        """ returns previous player """
        return self._prev_player

    def update(self, result):
        """ update node """
        self._wins = self._wins + result
        self._visits = self._visits + 1

    def choose_child_uct(self, exploration=math.sqrt(2)):
        """ We use the Upper Confidence Bound for Trees formula to select nodes to expand.
        Use the exploration parameter to balance exploitation and exploration. """
        # get the most promising child by selecting the child with the highest UCT value
        chosen_child = sorted(self._children,
                              # lambda function that calculates the value based on UCT
                              key=lambda child: child.get_wins() / child.get_visits()
                              + exploration * math.sqrt(math.log(self.get_visits())
                                                        / child.get_visits()))[-1]
        return chosen_child

    def child_add(self, move_tried, state):
        """ get rid of tried move from moves not tried and return added child. """
        # set node
        node = MCTSNode(move_tried, self, state)
        # remove from moves not tried of the node
        self._moves_not_tried.remove(move_tried)
        # add child
        self._children.append(node)

        return node


def agent_mcts(board, time_limit=1):
    """ tic tac toe agent that takes in a tic tac toe board object and returns
     the best move based on a Monte Carlo Tree Search agent. A time limit is set such
     that the best move after time_limit many seconds is returned. """

    # setting board state as the MCTS root node
    root = MCTSNode(state=board)

    # time limit for MCTS
    timeout = time.time() + time_limit

    while time.time() < timeout:  # loop is broken if time limit for search is exceeded

        node = root
        # make a copy of the board
        state = board.clone()

        # Step 1: Selection
        # whilst it is a not a terminal node and the node as no more expansions possible
        while node.get_moves_not_tried() == [] and node.get_children() != []:
            node = node.choose_child_uct()  # select and set node based on UCT formula
            state.place_move(node.get_move())

        # Step 2: Expansion
        # if the state is not terminal, we can still expand
        if node.get_moves_not_tried() != []:
            # choose a random move from moves we have not tried
            move = random.choice(node.get_moves_not_tried())
            state.place_move(move)
            node = node.child_add(move, state)

        # Step 3: Simulation
        state.rollout()

        # Step 4: Back-propagate from the node back to the root
        while node is not None:
            # update current node with other player's result
            node.update(state.get_curr_players_result(node.get_prev_player()))
            # work our way back up parent by parent back to the root
            node = node.get_parent()

    # return the move that was most visited
    selected_move = sorted(root.get_children(), key=lambda child: child.get_visits())[-1].get_move()
    return selected_move



def heur_pure_mc(board):
    """ pure Monte Carlo sim heuristic """
    if board.get_turn_counter() < 20:  # to save computation, first few moves just pick random
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
    if board.get_winner() == 1:
        return 1000000 - board.get_turn_counter()
    if board.get_winner() == 2:
        return -1000000 + board.get_turn_counter()
    return heuristic(board)






GAME_BOARD = TTTBoard()

# get difficulty of comp
while True:
    difficulty = int(input("Enter computer difficulty (1 to 10): "))
    if difficulty not in list(range(1, 11)):
        print("Illegal input. Enter difficulty (1 to 10): ")
    else:
        break

# initial random move
GAME_BOARD.place_move(random.randrange(1, 10))
print("current board:", GAME_BOARD.get_curr_board())
print(GAME_BOARD)

# game loop
while True:
    # players turn
    while True:
        move = int(input("Current sub-board is " + str(GAME_BOARD.get_curr_board()) + ". Enter a move: "))
        if move not in GAME_BOARD.get_moves():
            move = int(input("Illegal move. Enter move: "))
        else:
            break
    print("Player move: board", GAME_BOARD.get_curr_board(), "position", move)
    GAME_BOARD.place_move(move)
    print(GAME_BOARD)
    # check win
    if GAME_BOARD.get_winner():
        break

    # computers turn
    print("Robotossin is thinking...")
    print("DIFFICULTY IS", difficulty)
    move = agent_mcts(GAME_BOARD, time_limit=difficulty)
    print("Robotossin's move: board", GAME_BOARD.get_curr_board(), "position", move)
    GAME_BOARD.place_move(move)
    print(GAME_BOARD)
    # check win
    if GAME_BOARD.get_winner():
        break

# ending
winner = GAME_BOARD.get_winner()
if winner == 2:
    print("Lucky break, you won!")
elif winner == 1:
    print("You lose. Get better!")
else:
    print("You didn't lose. Draw!")