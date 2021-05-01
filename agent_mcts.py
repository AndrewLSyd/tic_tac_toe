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
