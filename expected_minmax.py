
from heuristic import EMPTY, ROWS, COLS, PLAYER1, PLAYER2, calculate_heuristic

INF = float('inf')


class ExpMinmax:
    def __init__(self, k):
        self.k = k
        self.dp = {}
        self.scores = []  # leaf node scores
        self.nodeExpansion = 0

    def is_valid_move(self, board, col):
        return board[0][col] == EMPTY

    def get_next_empty_row(self, board, col):
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == EMPTY:
                return row
        return -1

    def is_board_full(self, board):
        return not any(EMPTY in row for row in board)

    def expectiminimax(self, board, maximizing_player, alpha, beta, depth=None):
        if self.dp.get(board.tostring()) != None:
            return self.dp.get(board.tostring())
        if depth == 0 or self.is_board_full(board):  # Check if the board is full
            score = calculate_heuristic(board)  # Evaluate the board based on connected pieces
            self.scores.append(score)  # leaf node score
            self.dp[board.tostring()] = (score, None)
            return score, None

        if maximizing_player:
            max_eval = -INF
            move = None
            for col in range(COLS):
                if self.is_valid_move(board, col):
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row][col] = PLAYER2
                    if col == 0 or col == COLS - 1:  # Probability of 0.4 for first and last columns
                        prob = 0.4
                    else:
                        prob = 0.6  # Probability of 0.6 for other columns
                    if depth is not None and depth > 0:
                        self.nodeExpansion += 1
                        nvalue, nmove = prob * self.expectiminimax(temp_board, False, alpha, beta, depth - 1)
                    else:
                        nvalue, nmove = 0, None
                    if nvalue > max_eval:
                        max_eval = nvalue
                        move = col
                    alpha = max(alpha, nvalue)
                    if beta <= alpha:
                        break  # Beta cut-off
            self.dp[board.tostring()] = (max_eval, move)
            return nvalue, move
        else:
            min_eval = INF
            move = None
            for col in range(COLS):
                if self.is_valid_move(board, col):
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row][col] = PLAYER1
                    if col == 0 or col == COLS - 1:  # Probability of 0.4 for first and last columns
                        prob = 0.4
                    else:
                        prob = 0.6  # Probability of 0.6 for other columns

                    if depth is not None and depth > 0:
                        self.nodeExpansion += 1
                        nvalue, nmove = prob * self.expectiminimax(temp_board, True, alpha, beta,
                                                                     depth - 1)
                    else:
                        nvalue, nmove = 0, None
                    beta = min(beta, nvalue)
                    if beta <= alpha:
                        break  # Alpha cut-off
            self.dp[board.tostring()] = (min_eval, move)
            return min_eval, move

    def get_best_move(self, board):
        self.dp = {}
        self.scores = []  # leaf node scores
        return self.expectiminimax(board, True, -INF, INF)[1]

    def get_valid_moves(self, board):
        return [col for col in range(COLS) if self.is_valid_move(board, col)]

    def print_board(self, board):
        for row in board:
            print(row)
        print()

