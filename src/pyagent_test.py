"""
test module for py
"""
from pyagent import TTTBoard, mc_trial, pure_MC, final_heuristic, heur_twos, heur_centre

test_board = TTTBoard()

test_board.place(1, 4, 1)
test_board.place(1, 5, 1)
test_board.place(1, 9, 2)

test_board.place(2, 6, 1)

test_board.place(2, 4, 2)

test_board.place(3, 2, 1)
test_board.place(3, 5, 1)

test_board.place(4, 7, 1)
test_board.place(4, 8, 1)
test_board.place(4, 1, 2)
test_board.place(4, 3, 2)

test_board.place(5, 4, 1)
test_board.place(5, 9, 1)
test_board.place(5, 1, 2)
test_board.place(5, 7, 2)

test_board.place(6, 2, 2)
test_board.place(6, 5, 2)

test_board.place(7, 1, 1)
test_board.place(7, 2, 1)
test_board.place(7, 8, 2)

test_board.place(8, 9, 1)
test_board.place(8, 4, 2)
test_board.place(8, 7, 2)


test_board.place(9, 3, 2)
test_board.place(9, 5, 2)
print(test_board._players_turn)
test_board.place(9, 8, 1)
print(test_board._players_turn)
test_board.place(2, 1, 2)
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


test_board.place(test_board.get_curr_board(), 6)
print(test_board)





# print("winner of MC trial:", mc_trial(test_board, True))
# N_TRIALS = 1000
# scores = pure_MC(test_board)
# print(scores)
#
# test_board = TTTBoard()
# test_board.place(1, 7, 2)
# test_board.place(1, 8, 1)
#
# test_board.place(2, 1, 2)
#
# test_board.place(3, 5, 1)
#
# test_board.place(4, 3, 2)
#
# test_board.place(5, 4, 1)
# test_board.place(5, 8, 2)
#
# test_board.place(7, 8, 1)
#
# test_board.place(8, 2, 1)
# test_board.place(8, 5, 2)
# test_board.place(8, 9, 2)
#
# test_board.place(9, 5, 1)
# test_board.place(5, 2, 2)
#
# print(test_board)
#
# N_TRIALS = 50
# scores = pure_MC(test_board, 10, True)
# print(scores)


def test_doctest_check_win():
    """
    >>> test_board = TTTBoard()
    >>> print("test_0:", test_board.check_win())
    test_0: None\n
    Checking horizontal
    >>> test_board = TTTBoard()
    >>> test_board.place(2,1,2)
    >>> test_board.place(2,2,2)
    >>> test_board.place(2,3,2)
    >>> print("test_1:", test_board.check_win())
    test_1: 2\n
    >>> test_board = TTTBoard()
    >>> test_board.place(1,4,2)
    >>> test_board.place(1,5,2)
    >>> test_board.place(1,6,2)
    >>> print("test_2:", test_board.check_win())
    test_2: 2\n
    >>> test_board = TTTBoard()
    >>> test_board.place(2,7,2)
    >>> test_board.place(2,8,2)
    >>> test_board.place(2,9,2)
    >>> print("test_3:", test_board.check_win())
    test_3: 2\n
    Checking vertical
    >>> test_board = TTTBoard()
    >>> test_board.place(2,1,1)
    >>> test_board.place(2,4,1)
    >>> test_board.place(2,7,1)
    >>> print(test_board.check_win())
    1\n
    >>> test_board = TTTBoard()
    >>> test_board.place(2,2,1)
    >>> test_board.place(2,5,1)
    >>> test_board.place(2,8,1)
    >>> print(test_board.check_win())
    1\n
    >>> test_board = TTTBoard()
    >>> test_board.place(2,3,1)
    >>> test_board.place(2,6,1)
    >>> test_board.place(2,9,1)
    >>> print(test_board.check_win())
    1\n
    Checking diag
    >>> test_board = TTTBoard()
    >>> test_board.place(5,1,2)
    >>> test_board.place(5,5,2)
    >>> test_board.place(5,9,2)
    >>> print(test_board.check_win())
    2
    >>> test_board = TTTBoard()
    >>> test_board.place(5,3,2)
    >>> test_board.place(5,5,2)
    >>> test_board.place(5,7,2)
    >>> print(test_board.check_win())
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
    >>> test_board.place(1, 4, 1)
    >>> test_board.place(1, 5, 1)
    >>> test_board.place(1, 9, 2)
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
    >>> test_board.place(2, 1, 1)
    >>> test_board.place(2, 5, 1)
    >>> print(heur_twos(test_board))
    2
    >>> test_board.place(2, 9, 2)
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
    >>> test_board.place(5, 2, 2)
    >>> test_board.place(5, 5, 2)
    >>> test_board.place(5, 8, 2)
    >>> test_board.place(4, 3, 1)
    >>> test_board.place(4, 6, 1)
    >>> test_board.place(4, 9, 2)
    >>> print(heur_twos(test_board, True))
    [[1, 1], 0]
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
