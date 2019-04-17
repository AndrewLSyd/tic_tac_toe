N_TRIALS = 200

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


def pure_MC(board, num_trials=N_TRIALS):
    """ returns the pure Monte Carlo value of a board """
    score = 0
    for _ in range(num_trials):
        board_clone = board.clone()
        score += mc_trial(board_clone)
    return score
