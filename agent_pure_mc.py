"""
Pure Monte Carlo agent for tic tac toe
"""
import random
ILLEGAL_MOVE = -1_000_000_000  # arbitrarily low number to indicate illegal move


def mc_trial(board, verbose=False):
    """
    This function takes a current board and plays out the board randomly until the end.'
    2 is returned if player 1 wins, -2 is returned if player 2 wins and 0 if there is
    a draw.
    """
    move = board.get_rand_legal_move()  # initial move
    outcome = None

    while not outcome and move:  # while there is no winner and there is a valid move
        board.place_move(move)
        move = board.get_rand_legal_move()  # get new move
        outcome = board.get_winner()

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


def pure_MC(board, num_trials=200):
    """ returns the pure Monte Carlo value of a board """
    score = 0
    for _ in range(num_trials):
        board_clone = board.clone()
        score += mc_trial(board_clone)
    return score


def agent_pure_mc(board, sim_growth=0.02):
    """ pure monte carlo agent """
    move_values = [ILLEGAL_MOVE] * 9  # illegal moves set to arbitrarily low number
    for move in board.get_moves():
        board_clone = board.clone()
        board_clone.place_move(move)
        num_sims = 750 * (1 + sim_growth) ** board.get_turn_counter()
        # agent plays here and returns score of all moves
        move_values[move - 1] = pure_MC(board_clone, num_sims)
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
