import numpy as np

class Connect4Game:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.board = np.zeros((rows, columns))
        self.player = 1
        self.moves_left = columns * rows

    def play(self, column):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.player
                self.moves_left -= 1
                self.switch_player()
                return True
        return False    

    def switch_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1