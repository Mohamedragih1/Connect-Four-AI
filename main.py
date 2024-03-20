import numpy as np
import math

class Connect4Game:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.player = 1           # First player (1) or second (0)
        self.board = self.init_board()

    def init_board(self):
        return np.zeros((self.length, self.width), dtype=np.int8)

    def swap_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1     

    def play(self, column):
        board_column = self.board[:, column]
        for i in range(len(board_column)):
            if board_column[i] == 0:
                self.board[i][column] = self.player
                self.swap_player()
                break
            
    def play_AI(self): # Call Minmax
        pass
    
    def heuristic_evaluation(self):
        # Heuristic evaluation function to evaluate the current game state
        player = self.player
        opponent = 2 if player == 1 else 1

        player_score = 0
        opponent_score = 0

        # Evaluate rows
        for i in range(self.width):
            for j in range(self.length - 3):
                window = self.board[i, j:j+4]
                player_count = np.count_nonzero(window == player)
                opponent_count = np.count_nonzero(window == opponent)
                if player_count == 4:
                    return math.inf  # Player wins
                elif opponent_count == 4:
                    return -math.inf  # Opponent wins
                player_score += player_count ** 2
                opponent_score += opponent_count ** 2

        # Evaluate columns
        for i in range(self.width - 3):
            for j in range(self.length):
                window = self.board[i:i+4, j]
                player_count = np.count_nonzero(window == player)
                opponent_count = np.count_nonzero(window == opponent)
                if player_count == 4:
                    return math.inf  # Player wins
                elif opponent_count == 4:
                    return -math.inf  # Opponent wins
                player_score += player_count ** 2
                opponent_score += opponent_count ** 2

        # Evaluate diagonals (positive slope)
        for i in range(self.width - 3):
            for j in range(self.length - 3):
                window = [self.board[i+k][j+k] for k in range(4)]
                player_count = window.count(player)
                opponent_count = window.count(opponent)
                if player_count == 4:
                    return math.inf  # Player wins
                elif opponent_count == 4:
                    return -math.inf  # Opponent wins
                player_score += player_count ** 2
                opponent_score += opponent_count ** 2

        # Evaluate diagonals (negative slope)
        for i in range(self.width - 3):
            for j in range(3, self.length):
                window = [self.board[i+k][j-k] for k in range(4)]
                player_count = window.count(player)
                opponent_count = window.count(opponent)
                if player_count == 4:
                    return math.inf  # Player wins
                elif opponent_count == 4:
                    return -math.inf  # Opponent wins
                player_score += player_count ** 2
                opponent_score += opponent_count ** 2

        return player_score - opponent_score  # Heuristic evaluation score
    
    def terminal(self):
        # Check Rows
        for i in range(self.length):
            for j in range(self.width/2 + 1):
                if self.boar[i][j] == self.boar[i][j+1] == self.boar[i][j+2] == self.boar[i][j+3] == self.player:
                    return True
             
        # Check Columns
        for i in range(self.width):
            for j in range(self.length/2 + 1):
                if self.boar[i][j] == self.boar[i+1][j] == self.boar[i+2][j] == self.boar[i+3][j] == self.player:
                    return True
        
        # Check diagonals from bottom-left to top-right
        for i in range(self.width - 3):  
            for j in range(self.length - 3):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.player:
                    return True

        # Check diagonals from top-left to bottom-right
        for i in range(self.width - 3):  
            for j in range(3, self.length):
                if self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] == self.player:
                    return True
        
        return False
    

# def main():
#     connect4game = Connect4Game(7, 6)
#     print(connect4game.board)
#     connect4game.play(0)
#     print(connect4game.board)
#     connect4game.play(0)
#     print(connect4game.board)

#     connect4game.play(1)
#     print(connect4game.board)

# if __name__ == "__main__":
#     main()