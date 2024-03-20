import numpy as np
ROWS = 6
COLS = 7
MIN_WINNING_LENGTH = 4
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2


def evaluate_window(window, player):
    score = 0
    opponent = 3 - player  # Assuming only two players (1 and 2)

    player_count = np.count_nonzero(window == player)
    opponent_count = np.count_nonzero(window == opponent)
    empty_count = np.count_nonzero(window == EMPTY)

    # Calculate scores based on connected pieces
    if player_count >= MIN_WINNING_LENGTH:
        score += (player_count - MIN_WINNING_LENGTH + 1)  # Additional points for every extra connected piece beyond 4

    if opponent_count >= MIN_WINNING_LENGTH:
        score -= (opponent_count - MIN_WINNING_LENGTH + 1)   # Additional penalty for opponent having more than 4 connected pieces

    return score


def evaluate_board(board):
    score = 0
    center_weight = 2  # Weight for cells in the center

    # Iterate over all cells on the game board
    for row in range(ROWS):
        for col in range(COLS):
            # Calculate base score based on connected pieces
            if col <= COLS - MIN_WINNING_LENGTH:
                window = board[row, col:col+MIN_WINNING_LENGTH]
                score += evaluate_window(window, PLAYER1)

            if row <= ROWS - MIN_WINNING_LENGTH:
                window = board[row:row+MIN_WINNING_LENGTH, col]
                score += evaluate_window(window, PLAYER1)

            if row <= ROWS - MIN_WINNING_LENGTH and col <= COLS - MIN_WINNING_LENGTH:
                window = np.diag(board[row:row+MIN_WINNING_LENGTH, col:col+MIN_WINNING_LENGTH])
                score += evaluate_window(window, PLAYER1)

            if row <= ROWS - MIN_WINNING_LENGTH and col >= MIN_WINNING_LENGTH - 1:
                window = np.diag(np.fliplr(board[row:row+MIN_WINNING_LENGTH, col-MIN_WINNING_LENGTH+1:col+1]))
                score += evaluate_window(window, PLAYER1)

            # Adjust score based on cell's position in the center
            center_col = COLS // 2  # Center column
            center_row = ROWS // 2  # Center row

            if row == center_row and col == center_col:
                score += center_weight  # Add weight for center cell
            elif row == center_row - 1 or row == center_row + 1:
                if col == center_col - 1 or col == center_col + 1:
                    score += center_weight / 2  # Add half weight for adjacent cells to center
            elif row == center_row - 2 or row == center_row + 2:
                if col == center_col - 2 or col == center_col + 2:
                    score += center_weight / 3  # Add one-third weight for cells two positions away from center

    return score

