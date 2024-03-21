
from heuristic import EMPTY, ROWS, COLS, PLAYER1, PLAYER2, calculate_heuristic

INF = float('inf')


class Minmax:
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

    def minimax(self, board, maximizing_player, depth = None):
        if self.dp.get(board.tostring()) != None:
            return self.dp.get(board.tostring())
        if depth == None:
            depth = self.k
        if depth == 0 or self.is_board_full(board):  # Check if the board is full
            score = calculate_heuristic(board)  # Evaluate the board based on connected pieces
            self.scores.append(score) # leaf node score
            self.dp[board.tostring()] = (score, None)
            return score, None

        if maximizing_player:
            value = -INF
            move = None
            for col in range(COLS):
                if self.is_valid_move(board, col):
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row][col] = PLAYER2
                    self.nodeExpansion += 1
                    (nvalue, nmove) = self.minimax(temp_board, False, depth - 1)
                    if nvalue > value:
                        value = nvalue
                        move = col
            self.dp[board.tostring()] = (value, move)
            return value, move
        else:
            value = INF
            move = None
            for col in range(COLS):
                if self.is_valid_move(board, col):
                    temp_board = board.copy()
                    row = self.get_next_empty_row(temp_board, col)
                    temp_board[row][col] = PLAYER1
                    self.nodeExpansion += 1
                    (nvalue, nmove) = self.minimax(temp_board, True, depth - 1)
                    if nvalue < value:
                        value = nvalue
                        move = col
            self.dp[board.tostring()] = (value, move)
            return value, move

    def get_best_move(self, board):
        self.dp = {}
        self.scores = []  # leaf node scores
        return self.minimax(board, True)[1]


    def get_valid_moves(self, board):
        return [col for col in range(COLS) if self.is_valid_move(board, col)]

    def print_board(self, board):
        for row in board:
            print(row)
        print()



