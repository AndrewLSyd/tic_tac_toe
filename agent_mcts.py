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

    def choose_child_uct(self, exploration=math.sqrt(2)):
        """ We use the Upper Confidence Bound for Trees formula to select nodes to expand.
        We can use this to balance exploration vs exploitation. """
        # we can tune the exploration parameter here
        chosen_child = sorted(self._children,
                              key=lambda child: child.get_wins() / child.get_visits()
                              + exploration * math.sqrt(math.log(self.get_visits())
                                          / child.get_visits()))[-1]
        # get the most promising child by taking the one with the highest value
        return chosen_child

    def child_add(self, move_tried, state):
        """ get rid of tried move from moves not tried and return added child. """
        # set node
        node = MCTSNode(move=move_tried, parent=self, state=state)
        # remove from moves not tried of the node
        self._moves_not_tried.remove(move_tried)
        # add child
        self._children.append(node)

        return node

    def update(self, result):
        """ update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self._wins = self._wins + result
        self._visits = self._visits + 1

    def __repr__(self):
        out = "{Move - " + str(self._move) + " Wins/Visits:" + str(self._wins) + "/"\
                + str(self._visits) + " UCT:" + str(self._moves_not_tried) + "}"
        return out

    # def tree_as_string(self, indent):
    #     """
    #     :param indent: level of indent
    #     :return: returns a string representation of the tree
    #     """
    #     string_out = self.string_indent(indent) + str(self)
    #     for child in self._children:
    #         string_out += child.tree_as_string(indent + 1)
    #     return string_out
    #
    # def string_indent(self, indent):
    #     """
    #     :param indent: level of indent
    #     :return: returns indentation to represent the tree
    #     """
    #     string_out = "\n"
    #     for _ in range(1, indent + 1):
    #         string_out += "| "
    #     return string_out
    #
    # def children_as_string(self):
    #     string_out = ""
    #     for child in self._children:
    #         string_out += str(child) + "\n"
    #     return string_out


def uct(rootstate, time_limit, verbose=False):
    """ We use the upper confidence bound for trees search method here. """

    root = MCTSNode(state=rootstate)

    # time limit for MCTS
    timeout = time.time() + time_limit

    while time.time() < timeout:
        node = root
        state = rootstate.clone()

        # Step 1: Selection
        while node.get_moves_not_tried() == [] and node.get_children() != []:  # node is fully expanded and non-terminal
            node = node.choose_child_uct()
            state.place_move(node.get_move())

        # Step 2: Expansion
        if node.get_moves_not_tried() != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.get_moves_not_tried())
            state.place_move(m)
            node = node.child_add(m, state)  # add child and descend tree

        # Step 3: Simulation
        state.rollout()

        # Step 4: Back-propagate
        while node is not None:  # backpropagate from the expanded node and work back to the root node
            node.update(state.get_curr_players_result(
                node.get_prev_player()))  # state is terminal. update node with result from POV of node._prev_player
            node = node.get_parent()

    # Output some information about the tree - can be omitted
    # if verbose:
    #     print(root.tree_as_string(0))
    # else:
    #     print(root.children_as_string())

    return sorted(root.get_children(), key=lambda c: c.get_visits())[-1].get_move()  # return the move that was most visited


def agent_mcts(board, time_limit):
    """ We use the upper confidence bound for trees search method here. """

    root = MCTSNode(state=board)

    # time limit for MCTS
    timeout = time.time() + time_limit

    while time.time() < timeout:
        node = root
        state = board.clone()

        # Step 1: Selection
        while node.get_moves_not_tried() == [] and node.get_children() != []:  # node is fully expanded and non-terminal
            node = node.choose_child_uct()
            state.place_move(node.get_move())

        # Step 2: Expansion
        if node.get_moves_not_tried() != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.get_moves_not_tried())
            state.place_move(m)
            node = node.child_add(m, state)  # add child and descend tree

        # Step 3: Simulation
        state.rollout()

        # Step 4: Back-propagate
        while node is not None:  # backpropagate from the expanded node and work back to the root node
            node.update(state.get_curr_players_result(
                node.get_prev_player()))  # state is terminal. update node with result from POV of node._prev_player
            node = node.get_parent()

    # Output some information about the tree - can be omitted
    # if verbose:
    #     print(root.tree_as_string(0))
    # else:
    #     print(root.children_as_string())

    return sorted(root.get_children(), key=lambda c: c.get_visits())[-1].get_move()  # return the move that was most visited
