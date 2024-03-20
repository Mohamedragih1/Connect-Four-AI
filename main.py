import numpy as np
from heuristic import evaluate_board,EMPTY, ROWS, COLS, MIN_WINNING_LENGTH, PLAYER1, PLAYER2

def main():
    board = np.zeros((ROWS, COLS), dtype=int)
    game_over = False
    turn = 0
    k = int(input("Enter K:"))
    print("Welcome to Connect Four!")

    while not game_over:
        if turn % 2 == 0:
            col = get_best_move(board, k)  # AI player
            print(f"AI player plays column {col}")
            row = get_next_empty_row(board, col)
            board[row][col] = PLAYER2
        else:
            print_board(board)
            col = int(input("Player 1, choose a column (0-6): "))
            while col not in range(COLS) or not is_valid_move(board, col):
                col = int(input("Invalid move. Please choose a valid column (0-6): "))
            row = get_next_empty_row(board, col)
            board[row][col] = PLAYER1

        if is_winning_move(board, PLAYER1):
            print_board(board)
            print("Player 1 wins!")
            game_over = True
        elif is_winning_move(board, PLAYER2):
            print_board(board)
            print("AI player wins!")
            game_over = True
        elif len(get_valid_moves(board)) == 0:
            print_board(board)
            print("It's a tie!")
            game_over = True

        turn += 1


if __name__ == "__main__":
    main()