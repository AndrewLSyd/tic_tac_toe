"""
test module for py
"""
from pyagent import TTTBoard, mc_trial, pure_MC, final_heuristic, heur_twos, heur_centre, UCT


test_board = TTTBoard()

def UCTPlayGame():
    """ Play a sample game between two uct players where each player gets a different number
        of uct iterations (= simulations = tree nodes).
    """
    state = test_board
    while (state.get_moves() != []):
        if state.playerJustMoved == 1:
            m = UCT(rootstate=state, itermax=1000, verbose=False)  # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=1000, verbose=False)
        print("current board:", state.get_curr_board())
        print("Best Move: " + str(m) + "\n")
        state.place_move(m)
        print(state)
    if state.get_curr_players_result(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " num_wins!")
    elif state.get_curr_players_result(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " num_wins!")
    else:
        print("Nobody num_wins!")

UCTPlayGame()







test_board = TTTBoard()

test_board.place_move(board=1, num=4, player=1)
test_board.place_move(board=1, num=5, player=1)
test_board.place_move(board=1, num=9, player=2)

test_board.place_move(board=2, num=6, player=1)

test_board.place_move(board=2, num=4, player=2)

test_board.place_move(board=3, num=2, player=1)
test_board.place_move(board=3, num=5, player=1)

test_board.place_move(board=4, num=7, player=1)
test_board.place_move(board=4, num=8, player=1)
test_board.place_move(board=4, num=1, player=2)
test_board.place_move(board=4, num=3, player=2)

test_board.place_move(board=5, num=4, player=1)
test_board.place_move(board=5, num=9, player=1)
test_board.place_move(board=5, num=1, player=2)
test_board.place_move(board=5, num=7, player=2)

test_board.place_move(board=6, num=2, player=2)
test_board.place_move(board=6, num=5, player=2)

test_board.place_move(board=7, num=1, player=1)
test_board.place_move(board=7, num=2, player=1)
test_board.place_move(board=7, num=8, player=2)

test_board.place_move(board=8, num=9, player=1)
test_board.place_move(board=8, num=4, player=2)
test_board.place_move(board=8, num=7, player=2)


test_board.place_move(board=9, num=3, player=2)
test_board.place_move(board=9, num=5, player=2)
print(test_board._players_turn)
test_board.place_move(board=9, num=8, player=1)
print(test_board._players_turn)
test_board.place_move(board=2, num=1, player=2)
print(test_board._players_turn)
print(test_board)
print(final_heuristic(test_board))

children = test_board.get_child_boards()
print(children)
for child in children:
    print(child)

print("get rows")
print(test_board.get_rows(2))
print("get cols")
print(test_board.get_cols(2))


test_board.place_move(test_board.get_curr_board(), 6)
print(test_board)





# print("winner of MC trial:", mc_trial(test_board, True))
# N_TRIALS = 1000
# scores = pure_MC(test_board)
# print(scores)
#
# test_board = TTTBoard()
# test_board.place_move(board=1, 7, player=2)
# test_board.place_move(board=1, 8, player=1)
#
# test_board.place_move(board=2, 1, player=2)
#
# test_board.place_move(board=3, 5, player=1)
#
# test_board.place_move(board=4, 3, player=2)
#
# test_board.place_move(board=5, 4, player=1)
# test_board.place_move(board=5, 8, player=2)
#
# test_board.place_move(board=7, 8, player=1)
#
# test_board.place_move(board=8, 2, player=1)
# test_board.place_move(board=8, 5, player=2)
# test_board.place_move(board=8, 9, player=2)
#
# test_board.place_move(board=9, 5, player=1)
# test_board.place_move(board=5, 2, player=2)
#
# print(test_board)
#
# N_TRIALS = 50
# scores = pure_MC(test_board, 10, True)
# print(scores)


def test_doctest_check_win():
    """
    >>> test_board = TTTBoard()
    >>> print("test_0:", test_board.get_winner())
    test_0: None\n
    Checking horizontal
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=2, num=1, player=2)
    >>> test_board.place_move(board=2, num=2, player=2)
    >>> test_board.place_move(board=2, num=3, player=2)
    >>> print("test_1:", test_board.get_winner())
    test_1: 2\n
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=1, num=4, player=2)
    >>> test_board.place_move(board=1, num=5, player=2)
    >>> test_board.place_move(board=1, num=6, player=2)
    >>> print("test_2:", test_board.get_winner())
    test_2: 2\n
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=2, num=7, player=2)
    >>> test_board.place_move(board=2, num=8, player=2)
    >>> test_board.place_move(board=2, num=9, player=2)
    >>> print("test_3:", test_board.get_winner())
    test_3: 2\n
    Checking vertical
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=2, num=1, player=1)
    >>> test_board.place_move(board=2, num=4, player=1)
    >>> test_board.place_move(board=2, num=7, player=1)
    >>> print(test_board.get_winner())
    1\n
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=2, num=2, player=1)
    >>> test_board.place_move(board=2, num=5, player=1)
    >>> test_board.place_move(board=2, num=8, player=1)
    >>> print(test_board.get_winner())
    1\n
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=2, num=3, player=1)
    >>> test_board.place_move(board=2, num=6, player=1)
    >>> test_board.place_move(board=2, num=9, player=1)
    >>> print(test_board.get_winner())
    1\n
    Checking diag
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=5, num=1, player=2)
    >>> test_board.place_move(board=5, num=5, player=2)
    >>> test_board.place_move(board=5, num=9, player=2)
    >>> print(test_board.get_winner())
    2
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=5, num=3, player=2)
    >>> test_board.place_move(board=5, num=5, player=2)
    >>> test_board.place_move(board=5, num=7, player=2)
    >>> print(test_board.get_winner())
    2
    """

def test_get_row_col_diag():
    """
     0 0 0 | 0 0 0 | 0 0 0 |
     1 1 0 | 0 0 0 | 0 0 0 |
     0 0 2 | 0 0 0 | 0 0 0 |
     ------+-------+------
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     ------+-------+------
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
    >>> test_board = TTTBoard()
    >>> test_board.place_move(board=1, num=4, player=1)
    >>> test_board.place_move(board=1, num=5, player=1)
    >>> test_board.place_move(board=1, num=9, player=2)
    >>> print(test_board.get_rows(1))
    [array([0, 0, 0], dtype=int8), array([1, 1, 0], dtype=int8), array([0, 0, 2], dtype=int8)]
    >>> print(test_board.get_cols(1))
    [array([0, 1, 0], dtype=int8), array([0, 1, 0], dtype=int8), array([0, 0, 2], dtype=int8)]
    >>> print(test_board.get_diags(1))
    [array([0, 1, 2], dtype=int8), array([0, 1, 0], dtype=int8)]
    >>> print(heur_centre(test_board))
    1\n
     0 0 0 | 1 0 0 | 0 0 0 |
     1 1 0 | 0 1 0 | 0 0 0 |
     0 0 2 | 0 0 2 | 0 0 0 |
     ------+-------+------
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     ------+-------+------
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
    >>> test_board.place_move(board=2, num=1, player=1)
    >>> test_board.place_move(board=2, num=5, player=1)
    >>> print(heur_twos(test_board))
    2
    >>> test_board.place_move(board=2, num=9, player=2)
    >>> print(heur_twos(test_board))
    1
    >>> print(heur_centre(test_board))
    2\n
     0 0 0 | 1 0 0 | 0 0 0 |
     1 1 0 | 0 1 0 | 0 0 0 |
     0 0 2 | 0 0 2 | 0 0 0 |
     ------+-------+------
     0 0 1 | 0 2 0 | 0 0 0 |
     0 0 1 | 0 2 0 | 0 0 0 |
     0 0 2 | 0 2 0 | 0 0 0 |
     ------+-------+------
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
     0 0 0 | 0 0 0 | 0 0 0 |
    >>> test_board.place_move(board=5, num=2, player=2)
    >>> test_board.place_move(board=5, num=5, player=2)
    >>> test_board.place_move(board=5, num=8, player=2)
    >>> test_board.place_move(board=4, num=3, player=1)
    >>> test_board.place_move(board=4, num=6, player=1)
    >>> test_board.place_move(board=4, num=9, player=2)
    >>> print(heur_twos(test_board))
    0
    >>> print(heur_centre(test_board))
    1
    """

def test_heur_centre():
    """

    :return:
    """

# ===== DOCTEST =====
if __name__ == '__main__':
    import doctest

    doctest.testmod()
