from Piece import *

class Board:
    def __init__(self, board=1):
        self.rows = 8
        if board == 1:
            self.board = [[0 for x in range(self.rows)]for _ in range(self.rows)]
        else:
            self.board = board

    def update(self, screen):
        for x in range(8):
            for y in range(8):
                square = self.getSquare([x, y])
                if isinstance(square, King):
                    square.setCheck(square.isChecked(self))
                if isinstance(square, Piece):
                    square.draw(screen)


    def printBoard(self):
        for j in range(self.rows-1,-1,-1):
            for i in range(self.rows):
                print(self.board[i][j], end='')
            print("")

    def getSquare(self, pos):
        x = pos[0]
        y = pos[1]
        if x in range(8) and y in range(8):
            return self.board[x][y]
        return 0

    def loadBoard(self):

        # Pawns
        for x in range(8):
            wpawn = Pawn([x, 1], "w")
            bpawn = Pawn([x, 6], "b")
            self.addPiece(wpawn)
            self.addPiece(bpawn)

        # White pieces
        self.addPiece(Rook([0, 0], "w"))
        self.addPiece(Knight([1, 0], "w"))
        self.addPiece(Bishop([2, 0], "w"))
        self.addPiece(Queen([3, 0], "w"))
        self.addPiece(King([4, 0], "w"))
        self.addPiece(Bishop([5, 0], "w"))
        self.addPiece(Knight([6, 0], "w"))
        self.addPiece(Rook([7, 0], "w"))

        # Black pieces

        self.addPiece(Rook([0, 7], "b"))
        self.addPiece(Knight([1, 7], "b"))
        self.addPiece(Bishop([2, 7], "b"))
        self.addPiece(Queen([4, 7], "b"))
        self.addPiece(King([3, 7], "b"))
        self.addPiece(Bishop([5, 7], "b"))
        self.addPiece(Knight([6, 7], "b"))
        self.addPiece(Rook([7, 7], "b"))

    def addPiece(self, piece):
        x = piece.getPos()[0]
        y = piece.getPos()[1]
        self.board[x][y] = piece

    def addBlank(self, pos):
        if pos[0] in range(8) and pos[1] in range(8):
            self.board[pos[0]][pos[1]] = 0

    def getBoardCopy(self):
        board = [[0 for x in range(self.rows)] for _ in range(self.rows)]
        for x in range(8):
            for y in range(8):
                square = self.getSquare([x, y])
                if isinstance(square, Piece):
                    board[x][y] = square.getCopy()
        return board

    def testMove(self, origin, dest): # Returns true if move is valid
        testboard = Board(self.getBoardCopy())
        square = testboard.getSquare(origin)
        testboard.addBlank(origin)
        square.setPos(dest)
        testboard.addPiece(square)
        color = square.getColor()
        for x in range(8):
            for y in range(8):
                square = testboard.getSquare([x, y])
                if isinstance(square, King) and square.getColor() == color:
                    king = square
                    if king.isChecked(testboard):
                        return False
        return True




