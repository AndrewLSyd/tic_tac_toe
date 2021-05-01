import random
import agent_pure_mc
from agent_pure_mc import pure_MC

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
        return 1_000_000 - board.get_turn_counter()
    if board.get_winner() == 2:
        return -1_000_000 + board.get_turn_counter()
    return heuristic(board)
