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
print("Robotossin is impatient and goes first...")
GAME_BOARD.place_move(random.randrange(1, 10))
print("current board:", GAME_BOARD.get_curr_board())
print(GAME_BOARD)

# game loop
while True:
    # players turn
    while True:
        move = input("Boards and pieces are labelled 1 to 9 from left to right, top to bottom. Current sub-board is " + str(GAME_BOARD.get_curr_board()) + ". You are player 2. Enter a move: ")
        if (move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]) or (int(move) not in GAME_BOARD.get_moves()):
            print("Illegal move. Enter an integer between 1 and 9 in a position not already taken.")
            next
        else:
            move = int(move)  # cast to int
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
