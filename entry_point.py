from ttt_board import *
from agent_mcts import *
from agent_minimax import *

GAME_BOARD = TTTBoard()

# get difficulty of comp
while True:
    difficulty = int(input("Enter computer difficulty (1 to 10): "))
    if difficulty not in list(range(1, 11)):
        difficulty = print("Illegal input. Enter difficulty (1 to 10): ")
    else:
        break

# initial random move
GAME_BOARD.place_move(random.randrange(1, 10))
print("current board:", GAME_BOARD.get_curr_board())
print(GAME_BOARD)

# game loop
while True:
    # players turn
    while True:
        move = int(input("Current sub-board is " + str(GAME_BOARD.get_curr_board()) + ". Enter a move: "))
        if move not in GAME_BOARD.get_moves():
            move = int(input("Illegal move. Enter move: "))
        else:
            break
    print("Player move: board", GAME_BOARD.get_curr_board(), "position", move)
    GAME_BOARD.place_move(move)
    print(GAME_BOARD)
    # check win
    if GAME_BOARD.get_winner():
        break

    # computers turn
    print("Robotossin is thinking...")
    move = agent_mcts(GAME_BOARD, time_limit=difficulty)
    print("Robotossin's move: board", GAME_BOARD.get_curr_board(), "position", move)
    GAME_BOARD.place_move(move)
    print(GAME_BOARD)
    # check win
    if GAME_BOARD.get_winner():
        break

# ending
winner = GAME_BOARD.get_winner()
if winner == 2:
    print("Lucky break, you won!")
elif winner == 1:
    print("You lose. Get better!")
else:
    print("You didn't lose. Draw!")