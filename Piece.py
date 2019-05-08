import pygame

width = 500
height = 500

b_bishop = pygame.image.load("imgs\\b_bishop.png")
b_king = pygame.image.load("imgs\\b_king.png")
b_knight = pygame.image.load("imgs\\b_knight.png")
b_pawn = pygame.image.load("imgs\\b_pawn.png")
b_queen = pygame.image.load("imgs\\b_queen.png")
b_rook = pygame.image.load("imgs\\b_rook.png")

w_bishop = pygame.image.load("imgs\\w_bishop.png")
w_king = pygame.image.load("imgs\\w_king.png")
w_knight = pygame.image.load("imgs\\w_knight.png")
w_pawn = pygame.image.load("imgs\\w_pawn.png")
w_queen = pygame.image.load("imgs\\w_queen.png")
w_rook = pygame.image.load("imgs\\w_rook.png")


class Piece:

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.img = 0

    def move(self,pos,board):
        if pos in self.validMoves(board):
            self.pos = pos

    def validMoves(self, board):
        pass

    def draw(self,window):
        window.blit(self.img,self.getCoords(self.pos))

    def getCoords(self,pos):
        x = width/8 * pos[0]
        y = height - height/8 * (1+pos[1])
        return x,y

    def checkDiagonal(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]
        ran = range(0, 8)

        # UP RIGHT
        tempx = x + 1
        tempy = y + 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square == 0 or square.getColor == self.color:
                moves.append([tempx, tempy])
                tempx += 1
                tempy += 1
            else:
                break

        # DOWN RIGHT

        tempx = x + 1
        tempy = y - 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square == 0 or square.getColor == self.color:
                moves.append([tempx, tempy])
                tempx += 1
                tempy -= 1

        # DOWN LEFT

        tempx = x - 1
        tempy = y - 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square == 0 or square.getColor == self.color:
                moves.append([tempx, tempy])
                tempx -= 1
                tempy -= 1

        # UP LEFT

        tempx = x - 1
        tempy = y + 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square == 0 or square.getColor == self.color:
                moves.append([tempx, tempy])
                tempx -= 1
                tempy += 1
        return moves


class Bishop (Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_bishop
        else:
            self.img = w_bishop

    def __str__(self):

        if self.color == "b":
            return "bB"
        else:
            return "wB"

    def validMoves(self, board):
        return self.checkDiagonal(board)







