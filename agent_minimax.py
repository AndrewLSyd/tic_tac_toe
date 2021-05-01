"""
Minimax agent with alpha beta pruning
"""
import random
from heuristics import *


ILLEGAL_MOVE = -1_000_000_000  # arbitrarily low number to indicate illegal move


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
