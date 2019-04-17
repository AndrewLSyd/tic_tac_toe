import time
import random
import math

class Node:
    """ A node in the game tree. Node wins is always from the viewpoint of _prev_player.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self._move = move  # the move that got us to this node - "None" for the root node
        self._parent = parent  # "None" for the root node
        self._child = []
        self._wins = 0
        self._visits = 0
        self.untriedMoves = state.get_moves()  # future child nodes
        self._prev_player = state.prev_player  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c._wins/c._visits + UCTK * sqrt(2*log(self._visits)/c._visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self._child, key=lambda c: c._wins / c._visits + math.sqrt(2 * math.log(self._visits) / c._visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self._child.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self._visits += 1
        self._wins += result

    def __repr__(self):
        return "[M:" + str(self._move) + " W/V:" + str(self._wins) + "/" + str(self._visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self._child:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self._child:
            s += str(c) + "\n"
        return s


def UCT(rootstate, time_limit, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    timeout = time.time() + time_limit

    while time.time() < timeout:
        node = rootnode
        state = rootstate.clone()

        # Select
        while node.untriedMoves == [] and node._child != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.place_move(node._move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.place_move(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_moves() != []:  # while state is non-terminal
            state.place_move(random.choice(state.get_moves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.get_curr_players_result(
                node._prev_player))  # state is terminal. Update node with result from POV of node._prev_player
            node = node._parent

    # Output some information about the tree - can be omitted
    if verbose:
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sorted(rootnode._child, key=lambda c: c._visits)[-1]._move  # return the move that was most visited


def agent_mcts(board, time_limit):
    """
    :param board: game state
    :return: best move [1, 0]
    """
    return UCT(rootstate=board, time_limit=time_limit, verbose=False)
