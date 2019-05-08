class Board:
    def __init__(self):
        self.rows = 8
        self.board = [[0 for x in range(self.rows)]for _ in range(self.rows)]
        self.board[0][6] = 0

    def update(self):
        pass

    def printBoard(self):
        for i in range(self.rows-1,-1,-1):
            for j in range(self.rows):
                print(self.board[i][j], end='')
            print("")

    def getSquare(self, pos):
        x = pos[0]
        y = pos[1]
        return self.board[x][y]