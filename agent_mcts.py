"""
Tic Tac Toe agent that uses a Monte Carlo Tree Search
"""
import time
import random
import math


class Node:
    """
        Class for Node in the Monte Carlo Tree Search
    """

    def __init__(self, move=None, parent=None, state=None):
        # move that got us here
        self._move = move
        # parent node
        self._parent = parent
        self._children = []
        self._visits = 0
        self._wins = 0
        self._moves_not_tried = state.get_moves()  # future child nodes
        self._prev_player = state.prev_player  # the only part of the state that the Node needs later

    def get_wins(self):
        return self._wins

    def get_visits(self):
        return self._visits

    def choose_child_uct(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda child: child._wins/child._visits + UCTK * sqrt(2*log(self._visits)/child._visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self._children, key=lambda child: child.get_wins() / child.get_visits() + math.sqrt(2 * math.log(self.get_visits()) / child.get_visits()))[-1]
        return s

    def child_add(self, m, s):
        """ Remove m from _moves_not_tried and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self._moves_not_tried.remove(m)
        self._children.append(n)
        return n

    def update(self, result):
        """ update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self._visits += 1
        self._wins += result

    def __repr__(self):
        return "[M:" + str(self._move) + " W/V:" + str(self._wins) + "/" + str(self._visits) + " U:" + str(
            self._moves_not_tried) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self._children:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self._children:
            s += str(c) + "\n"
        return s


def UCT(rootstate, time_limit, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    # time limit for MCTS
    timeout = time.time() + time_limit

    while time.time() < timeout:
        node = rootnode
        state = rootstate.clone()

        # Select
        while node._moves_not_tried == [] and node._children != []:  # node is fully expanded and non-terminal
            node = node.choose_child_uct()
            state.place_move(node._move)

        # Expand
        if node._moves_not_tried != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node._moves_not_tried)
            state.place_move(m)
            node = node.child_add(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_moves() != []:  # while state is non-terminal
            state.place_move(random.choice(state.get_moves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.update(state.get_curr_players_result(
                node._prev_player))  # state is terminal. update node with result from POV of node._prev_player
            node = node._parent

    # Output some information about the tree - can be omitted
    if verbose:
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sorted(rootnode._children, key=lambda c: c._visits)[-1]._move  # return the move that was most visited


def agent_mcts(board, time_limit):
    """
    :param board: game state
    :return: best move [1, 0]
    """
    return UCT(rootstate=board, time_limit=time_limit, verbose=False)
