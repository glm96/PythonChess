import pygame

width = 500
height = 500

b_bishop = pygame.image.load("img\\b_bishop.png")
b_king = pygame.image.load("img\\b_king.png")
b_king_checked = pygame.image.load("img\\b_king_checked.png")
b_knight = pygame.image.load("img\\b_knight.png")
b_pawn = pygame.image.load("img\\b_pawn.png")
b_queen = pygame.image.load("img\\b_queen.png")
b_rook = pygame.image.load("img\\b_rook.png")

w_bishop = pygame.image.load("img\\w_bishop.png")
w_king = pygame.image.load("img\\w_king.png")
w_king_checked = pygame.image.load("img\\w_king_checked.png")
w_knight = pygame.image.load("img\\w_knight.png")
w_pawn = pygame.image.load("img\\w_pawn.png")
w_queen = pygame.image.load("img\\w_queen.png")
w_rook = pygame.image.load("img\\w_rook.png")




class Piece:

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.img = 0

    def setPos(self, pos):
        self.pos = pos

    def move(self,pos,board):
        if pos in self.validMoves(board):
            x = self.pos[0]
            y = self.pos[1]
            board.addBlank([x, y])
            self.pos = pos
            board.addPiece(self)
            return True
        else:
            return False

    def validMoves(self, board):
        pass

    def draw(self,window):
        window.blit(self.img,self.getCoords(self.pos))

    def getCoords(self,pos):
        x = width/8 * (pos[0])
        y = height - height/8 * (1+pos[1])
        return x,y

    def getPos(self):
        return self.pos[0],self.pos[1]

    def checkDiagonal(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]
        ran = range(8)

        # UP RIGHT
        tempx = x + 1
        tempy = y + 1

        while tempx in ran and tempy in ran:
            if self.isValid(self.color, [tempx, tempy], board):
                moves.append([tempx, tempy])
                if board.getSquare([tempx, tempy]) != 0:  # Reached a piece
                    break
            tempx += 1
            tempy += 1

        # DOWN RIGHT

        tempx = x + 1
        tempy = y - 1

        while tempx in ran and tempy in ran:
            if self.isValid(self.color, [tempx, tempy], board):
                moves.append([tempx, tempy])
                if board.getSquare([tempx, tempy]) != 0:  # Reached a piece
                    break
            tempx += 1
            tempy -= 1
        # DOWN LEFT

        tempx = x - 1
        tempy = y - 1

        while tempx in ran and tempy in ran:
            if self.isValid(self.color, [tempx, tempy], board):
                moves.append([tempx, tempy])
                if board.getSquare([tempx, tempy]) != 0:  # Reached a piece
                    break
            tempx -= 1
            tempy -= 1
        # UP LEFT

        tempx = x - 1
        tempy = y + 1

        while tempx in ran and tempy in ran:
            if self.isValid(self.color, [tempx, tempy], board):
                moves.append([tempx, tempy])
                if board.getSquare([tempx, tempy]) != 0:  # Reached a piece
                    break
            tempx -= 1
            tempy += 1
        return moves

    def checkPerpendicular(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]

        # Check left
        for tx in range(self.pos[0]-1, -1, -1):
            if self.isValid(self.color, [tx, y], board):
                square = board.getSquare([tx, y])
                moves.append([tx, y])
                if square != 0:  # reached a piece
                    break

        # Check right

        for tx in range(self.pos[0]+1, 8, 1):
            if self.isValid(self.color, [tx, y], board):
                square = board.getSquare([tx, y])
                moves.append([tx, y])
                if square != 0:  # reached a piece
                    break
        # Check up
        for ty in range(self.pos[1]+1, 8, 1):
            if self.isValid(self.color, [x, ty], board):
                square = board.getSquare([x, ty])
                moves.append([x, ty])
                if square != 0:  # reached a piece
                    break


        # Check up
        for ty in range(self.pos[1]-1, -1, -1):
            if self.isValid(self.color, [x, ty], board):
                square = board.getSquare([x, ty])
                moves.append([x, ty])
                if square != 0:  # reached a piece
                    break

        return moves

    def getColor(self):
        return self.color

    def isValid(self, color, move, board):
        if not (move[0] in range(0,8) and move[1] in range(0,8)):
            return False
        square = board.getSquare(move)
        if square == 0 or square.getColor() != color:
            if board.testMove(self.pos, move):
                return True

        return False


    def getCopy(self):
        pass


class Bishop (Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_bishop
        else:
            self.img = w_bishop

    def __str__(self):
        return self.color + "B"

    def validMoves(self, board):
        return self.checkDiagonal(board)

    def getCopy(self):
        return Bishop(self.pos, self.color)


class King (Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_king
        else:
            self.img = w_king
        self.checked = False

    def __str__(self):
        return self.color + "K"

    def draw(self,window):
        if self.getColor() == "w":
            if self.checked:
                img = w_king_checked
            else:
                img = w_king
        else:
            if self.checked:
                img = b_king_checked
            else:
                img = b_king
        window.blit(img,self.getCoords(self.pos))

    def setCheck(self, check):
        self.checked = check

    def validMoves(self, board):
        moves = []
        validmoves = []
        x = self.pos[0]
        y = self.pos[1]
        for tx in range(x-1, x+2):
            if tx in range(0, 7):
                for ty in range(y-1, y+2):
                    if ty in range(0, 7):
                        if not (tx == x and ty == y):
                            moves.append([tx, ty])
        for move in moves:
            if self.isValid(self.color, move, board):
                validmoves.append(move)
        return validmoves

    def isChecked(self, board):
        x = self.getPos()[0]
        y = self.getPos()[1]
        if self.getColor() == "w":
            mod = 1
        else:
            mod = -1
        # Check Bishop + Queen diagonal
        for pos in self.checkDiagonal(board):
            square = board.getSquare(pos)
            if isinstance(square, (Bishop, Queen)) and square.getColor() != self.getColor():
                return True
        # Check Rook + Queen line
        for pos in self.checkPerpendicular(board):
            square = board.getSquare(pos)
            if isinstance(square, (Rook, Queen)) and square.getColor() != self.getColor():
                return True
        # Check Knight
        for pos in self.getKnightMoves(board):
            square = board.getSquare(pos)
            if isinstance(square, Knight):
                if square.getColor() != self.getColor():
                    return True
        # Check opposing King
        for tx in range(x-1,x+2,1):
            if tx in range(8):
                for ty in range(y-1, y+2, 1):
                    if ty in range(8):
                        square = board.getSquare([x, y])
                        if isinstance(square, King) and square.getColor() != self.getColor():
                            return True
        # Check for pawns
        for tx in [x-1, x+1]:
            if tx in range(8) and y+mod in range(8):
                square = board.getSquare([tx, y+mod])
                if isinstance(square, Pawn):
                    if square.getColor() != self.getColor():
                        return True
        return False

    def getKnightMoves(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]
        # Far left and far right moves
        for ty in [y - 1, y + 1]:
            for tx in [x + 2, x - 2]:
                if board.getSquare([tx, ty]) != 0:
                    moves.append([tx, ty])
        # top right and top left moves
        for ty in [y - 2, y + 2]:
            for tx in [x + 1, x - 1]:
                if board.getSquare([tx, ty]) != 0:
                    moves.append([tx, ty])
        return moves

    def checkDiagonal(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]
        ran = range(8)
        # UP RIGHT
        tempx = x + 1
        tempy = y + 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square != 0:
                moves.append([tempx, tempy])
                break
            else:
                tempx = tempx + 1
                tempy = tempy + 1

        # DOWN RIGHT

        tempx = x + 1
        tempy = y - 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square != 0:
                moves.append([tempx, tempy])
                break
            else:
                tempx = tempx + 1
                tempy = tempy - 1
        # DOWN LEFT

        tempx = x - 1
        tempy = y - 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square != 0:
                moves.append([tempx, tempy])
                break
            else:
                tempx = tempx - 1
                tempy = tempy + 1
        # UP LEFT

        tempx = x - 1
        tempy = y + 1

        while tempx in ran and tempy in ran:
            square = board.getSquare([tempx, tempy])
            if square != 0:
                moves.append([tempx, tempy])
                break
            else:
                tempx -= 1
                tempy += 1
        return moves

    def checkPerpendicular(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]

        # Check left
        for tx in range(self.pos[0] - 1, -1, -1):
            square = board.getSquare([tx, y])
            if square != 0:
                moves.append([tx, y])
                break

        # Check right

        for tx in range(self.pos[0] + 1, 8, 1):
            square = board.getSquare([tx, y])
            if square != 0:
                moves.append([tx, y])
                break

        # Check up
        for ty in range(self.pos[1] + 1, 8, 1):
            square = board.getSquare([x, ty])
            if square != 0:
                moves.append([x, ty])
                break

        # Check up
        for ty in range(self.pos[1] - 1, -1, -1):
            square = board.getSquare([x, ty])
            if square != 0:
                moves.append([x, ty])
                break

        return moves

    def getCopy(self):
        return King(self.pos, self.color)


class Knight (Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_knight
        else:
            self.img = w_knight

    def __str__(self):
        return self.color + "N"

    def validMoves(self, board):
        moves = []
        x = self.pos[0]
        y = self.pos[1]

        # Far left and far right moves
        for ty in [y-1, y+1]:
            for tx in [x+2, x-2]:
                if self.isValid(self.getColor(), [tx, ty], board):
                    moves.append([tx, ty])
        # top right and top left moves
        for ty in [y-2, y+2]:
            for tx in [x+1, x-1]:
                if self.isValid(self.getColor(), [tx, ty], board):
                    moves.append([tx, ty])
        return moves

    def getCopy(self):
        return Knight(self.pos, self.color)


class Pawn (Piece):

    def __init__(self, pos, color, passant=False):
        Piece.__init__(self, pos, color)
        self.passant = passant # Flag for en passant moves against the piece
        if color == "b":
            self.img = b_pawn
        else:
            self.img = w_pawn

    def __str__(self):
        return self.color + "P"

    def getPassant(self):
        return self.passant

    def clearPassant(self):
        self.passant = False

    def move(self,pos,board):
        if pos in self.validMoves(board):
            x = self.pos[0]
            y = self.pos[1]
            if abs(y-pos[1]) == 2:
                self.passant = True
            board.addBlank([x, y])
            self.pos = pos
            board.addPiece(self)
            return True
        else:
            return False

    def isValid(self, color, move, board):
        if not (move[0] in range(0,8) and move[1] in range(0,8)):
            return False
        square = board.getSquare(move)
        x = move[0]

        if x == self.pos[0]: # Taking a piece
            if square == 0:
                if board.testMove(self.pos, move):
                    return True
        else: # Moving forwards
            if square != 0 and square.getColor() != self.color:
                if board.testMove(self.pos, move):
                    return True
        return False

    def validMoves(self, board):
        moves = []
        validmoves = []
        x = self.pos[0]
        y = self.pos[1]
        mod = 1 # 1 for white, -1 for black
        if self.getColor() == "b":
            mod = -1
        if (y == 1 and mod == 1) or (y == 6 and mod == -1):
                moves.append([x, y+(mod * 2)])
        for tx in range(x-1,x+2,1):
            moves.append([tx, y + mod])
        for move in moves:
            if self.isValid(self.color, move, board):
                validmoves.append(move)
        # Check for en passant captures
        if x > 0:
            square = board.getSquare([x - 1, y])
            if self.checkPassant(square):
                if board.getSquare([x - 1, y + mod]) == 0:
                    validmoves.append([x - 1, y + mod])
        if x < 7:
            square = board.getSquare([x + 1, y])
            if self.checkPassant(square):
                if board.getSquare([x + 1, y + mod]) == 0:
                    validmoves.append([x + 1, y + mod])

        return validmoves

    def checkPassant(self,square):
        if square == 0:
            return False
        if self.color == "w":
            color = "b"
        else:
            color = "w"
        if str(square) == color + "P":
            if square.getPassant():
                return True

    def getCopy(self):
        return Pawn(self.pos, self.color, self.getPassant())


class Queen (Piece):
    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_queen
        else:
            self.img = w_queen

    def __str__(self):
        return self.color + "Q"

    def validMoves(self, board):
        moves = self.checkDiagonal(board)
        for move in self.checkPerpendicular(board):
            moves.append(move)
        return moves

    def getCopy(self):
        return Queen(self.pos, self.color)


class Rook (Piece):
    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_rook
        else:
            self.img = w_rook

    def __str__(self):
        return self.color + "R"

    def validMoves(self, board):
        moves = self.checkPerpendicular(board)
        return moves

    def getCopy(self):
        return Rook(self.pos, self.color)
