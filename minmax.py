import numpy as np
import random
from heuristic import evaluate_board,EMPTY, ROWS, COLS, MIN_WINNING_LENGTH, PLAYER1, PLAYER2
from test import calculate_heuristic, find_score

INF = float('inf')


def is_valid_move(board, col):
    return board[0][col] == EMPTY


def get_next_empty_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return -1


def is_board_full(board):
    return not any(EMPTY in row for row in board)


def expectiminimax(board, depth, maximizing_player, max_depth, alpha, beta):
    if depth == 0 or is_board_full(board):  # Check if the board is full
        score = calculate_heuristic(board)  # Evaluate the board based on connected pieces
        return score

    if maximizing_player:
        value = -INF
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                row = get_next_empty_row(temp_board, col)
                temp_board[row][col] = PLAYER2
                value = max(value, expectiminimax(temp_board, depth-1, False, max_depth, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
        return value
    else:
        if depth == max_depth:
            column_probabilities = [0.2 if col == 0 or col == COLS-1 else 0.6 for col in range(COLS)]
            random_column = random.choices(range(COLS), weights=column_probabilities)[0]
            if is_valid_move(board, random_column):
                temp_board = board.copy()
                row = get_next_empty_row(temp_board, random_column)
                temp_board[row][random_column] = PLAYER1
                return expectiminimax(temp_board, depth-1, True, max_depth, alpha, beta)
            else:
                return 0  # Invalid move, return 0
        else:
            value = INF
            for col in range(COLS):
                if is_valid_move(board, col):
                    temp_board = board.copy()
                    row = get_next_empty_row(temp_board, col)
                    temp_board[row][col] = PLAYER1
                    value = min(value, expectiminimax(temp_board, depth-1, True, max_depth, alpha, beta))
                    beta = min(beta, value)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return value


def minimax_pruning(board, depth, maximizing_player, max_depth, alpha, beta):
    if depth == 0 or is_board_full(board):  # Check if the board is full
        score = calculate_heuristic(board)  # Evaluate the board based on connected pieces
        return score

    if maximizing_player:
        value = -INF
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                row = get_next_empty_row(temp_board, col)
                temp_board[row][col] = PLAYER2
                value = max(value, minimax_pruning(temp_board, depth-1, False, max_depth, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
        return value
    else:
        value = INF
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                row = get_next_empty_row(temp_board, col)
                temp_board[row][col] = PLAYER1
                value = min(value, expectiminimax(temp_board, depth-1, True, max_depth, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
        return value

def minimax(board, depth, maximizing_player, max_depth):
    if depth == 0 or is_board_full(board):  # Check if the board is full
        score = calculate_heuristic(board)  # Evaluate the board based on connected pieces
        return score

    if maximizing_player:
        value = -INF
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                row = get_next_empty_row(temp_board, col)
                temp_board[row][col] = PLAYER2
                value = max(value, minimax(temp_board, depth-1, False, max_depth))
        return value
    else:
        value = INF
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                row = get_next_empty_row(temp_board, col)
                temp_board[row][col] = PLAYER1
                value = min(value, minimax(temp_board, depth-1, True, max_depth))
        return value


def get_best_move(board, depth):
    best_score = -INF
    best_col = None
    
    # Test every move
    for col in range(COLS):
        if is_valid_move(board, col):
            temp_board = board.copy()
            row = get_next_empty_row(temp_board, col)  # Find the lowest empty row in the column
            temp_board[row][col] = PLAYER2  # Place the AI player's piece in that row and column
            score = minimax_pruning(temp_board, depth - 1, False, depth,-INF, INF)  # Pass depth limit

            # Debug prints
            print(f"Move: {col}, Score: {score}")

            if score > best_score:
                best_score = score
                best_col = col  # Update the best column if a higher-scoring move is found
    return best_col


def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]


def print_board(board):
    for row in board:
        print(row)
    print()


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
        print(find_score(board))
        if len(get_valid_moves(board)) == 0:
            print_board(board)
            game_over = True
            print(find_score(board))

        turn += 1


if __name__ == "__main__":
    main()