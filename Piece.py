import pygame

width = 500
height = 500

# Loading images for all pieces
b_bishop = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_bishop.png")
b_king = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_king.png")
b_king_checked = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_king_checked.png")
b_knight = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_knight.png")
b_pawn = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_pawn.png")
b_queen = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_queen.png")
b_rook = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\b_rook.png")

w_bishop = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_bishop.png")
w_king = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_king.png")
w_king_checked = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_king_checked.png")
w_knight = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_knight.png")
w_pawn = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_pawn.png")
w_queen = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_queen.png")
w_rook = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\w_rook.png")


class Piece:
    """
    Parent class for all pieces
    """
    def __init__(self, pos, color):
        """
        Piece initialization
        :param pos: Current position of the piece
        :param color: Color of the piece
        """
        self.pos = pos
        self.color = color
        self.img = 0

    def set_pos(self, pos):
        """
        Setter for piece position

        :param pos: New position for the piece
        """
        self.pos = pos

    def move(self, pos, board):
        """
        Basic move of a piece

        :param pos: Position to move to
        :param board: Board in which the piece is to be stored
        """
        x, y = self.get_pos()
        board.add_blank([x, y])
        self.pos = pos
        board.add_piece(self)

    def is_taking(self, board, move):
        """
        Checks whether the piece is making a taking move for PGN purposes

        :param board: Board where pieces are stored
        :param move: Move made
        """
        if board.get_square(move) == 0:
            return False
        return True

    def get_FEN(self):
        """
        Returns the piece's representation in FEN format (Black lowercase, white uppercase)

        :return: FEN string of the piece
        """
        s = str(self)
        if self.color == "b":
            s = str(self).lower()
        return s

    def valid_moves(self, board):
        """
        Returns a list of valid moves for the specified piece

        :param board: Board where the piece is located
        :return: List with valid moves
        """
        pass

    def draw(self, window):
        """
        Draw the piece's image onto the board

        :param window: PyGame screen object
        """
        window.blit(self.img, self.get_coords(self.pos))

    @staticmethod
    def get_coords(pos):
        """
        Returns coordinates as (x,y) relative to window size

        :param pos: Position to convert
        :return: X and Y parameters of the position
        """
        x = width/8 * (pos[0])
        y = height - height/8 * (1+pos[1])
        return x, y

    def get_pos(self):
        """
        Getter for piece position

        :return: Current position of the piece
        """
        return self.pos[0], self.pos[1]

    def check_diagonal(self, board):
        """
        Method for checking whether there are valid moves in all four diagonals

        :param board: Board where the piece is located
        :return: list with all valid moves
        """
        moves = []
        x, y = self.get_pos()
        ran = range(8)

        # UP RIGHT
        temp_x = x + 1
        temp_y = y + 1

        while temp_x in ran and temp_y in ran:
            if self.is_valid(self.color, [temp_x, temp_y], board):
                moves.append([temp_x, temp_y])
            square = board.get_square([temp_x, temp_y])
            if isinstance(square, Piece):  # Reached a piece
                break
            temp_x += 1
            temp_y += 1

        # DOWN RIGHT

        temp_x = x + 1
        temp_y = y - 1

        while temp_x in ran and temp_y in ran:
            if self.is_valid(self.color, [temp_x, temp_y], board):
                moves.append([temp_x, temp_y])
            square = board.get_square([temp_x, temp_y])
            if isinstance(square, Piece):  # Reached a piece
                break
            temp_x += 1
            temp_y -= 1
        # DOWN LEFT

        temp_x = x - 1
        temp_y = y - 1

        while temp_x in ran and temp_y in ran:
            if self.is_valid(self.color, [temp_x, temp_y], board):
                moves.append([temp_x, temp_y])
            square = board.get_square([temp_x, temp_y])
            if isinstance(square, Piece):  # Reached a piece
                break
            temp_x -= 1
            temp_y -= 1
        # UP LEFT

        temp_x = x - 1
        temp_y = y + 1

        while temp_x in ran and temp_y in ran:
            if self.is_valid(self.color, [temp_x, temp_y], board):
                moves.append([temp_x, temp_y])
            square = board.get_square([temp_x, temp_y])
            if isinstance(square, Piece):  # Reached a piece
                break
            temp_x -= 1
            temp_y += 1
        return moves

    def check_perpendicular(self, board):
        """
        Method for checking whether there are valid moves in all four straight lines

        :param board: Board where the piece is located
        :return: list with all valid moves
        """
        moves = []
        x, y = self.get_pos()

        # Check left
        for tx in range(self.pos[0]-1, -1, -1):
            if self.is_valid(self.color, [tx, y], board):
                moves.append([tx, y])
            square = board.get_square([tx, y])
            if isinstance(square, Piece):  # reached a piece
                break

        # Check right

        for tx in range(self.pos[0]+1, 8, 1):
            if self.is_valid(self.color, [tx, y], board):
                moves.append([tx, y])
            square = board.get_square([tx, y])
            if isinstance(square, Piece):  # reached a piece
                break
        # Check up
        for ty in range(self.pos[1]+1, 8, 1):
            if self.is_valid(self.color, [x, ty], board):
                moves.append([x, ty])
            square = board.get_square([x, ty])
            if isinstance(square, Piece):  # reached a piece
                break

        # Check up
        for ty in range(self.pos[1]-1, -1, -1):
            if self.is_valid(self.color, [x, ty], board):
                moves.append([x, ty])
            square = board.get_square([x, ty])
            if isinstance(square, Piece):  # reached a piece
                break

        return moves

    def get_color(self):
        """
        Getter for piece color

        :return: A string with "w" or "b" representing the color of the piece
        """
        return self.color

    def is_valid(self, color, move, board):
        """
        Tests whether a specified move is or not valid

        :param color: Color of the current piece
        :param move: Move to be tested
        :param board: Board where the piece is located
        :return: True if the move is valid
        """
        if not (move[0] in range(0, 8) and move[1] in range(0, 8)):
            return False
        square = board.get_square(move)
        if square == 0 or square.get_color() != color:
            if board.test_move(self.pos, move):
                return True

        return False

    def get_copy(self):
        """
        Returns an identical piece

        :return: A Piece object with the same parameters
        """
        pass


class Bishop (Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_bishop
        else:
            self.img = w_bishop

    def __str__(self):
        return "B"

    def valid_moves(self, board):
        return self.check_diagonal(board)

    def get_copy(self):
        return Bishop(self.pos, self.color)


class King (Piece):

    def __init__(self, pos, color, cast=True, checked=False):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_king
        else:
            self.img = w_king
        self.checked = checked
        self.castleable = cast

    def __str__(self):
        return "K"

    def draw(self, window):
        if self.get_color() == "w":
            if self.checked:
                img = w_king_checked
            else:
                img = w_king
        else:
            if self.checked:
                img = b_king_checked
            else:
                img = b_king
        window.blit(img, self.get_coords(self.pos))

    def move(self, pos, board):
        x, y = self.get_pos()
        # Check if move is castling
        if abs(pos[0]-x) == 2:
            if not self.castle(pos, board):  # Castling didn't go well
                print("Error on castling logic")
                return False
            return True
        else:
            if pos in self.valid_moves(board):
                board.add_blank([x, y])
                self.pos = pos
                board.add_piece(self)
                if self.can_castle():
                    self.flag_uncastleable()
                return True
            else:
                return False

    def castle(self, pos, board):
        """
        Handles castling movements

        :param pos: Position to move to
        :param board: Board the move is being made on
        :return: True if castled correctly
        """

        x, y = self.get_pos()
        # Get the involved rook
        if pos[0] < x:  # Left castling
            rook_x = 0
            new_x = pos[0]+1
        else:  # Right castling
            rook_x = 7
            new_x = pos[0]-1
        rook = board.get_square([rook_x, y])
        if isinstance(rook, Rook) and rook.get_color() == self.get_color():  # Ensure rook is correct
            self.flag_uncastleable()
            board.add_blank(self.get_pos())
            board.add_blank(rook.get_pos())
            self.pos = pos
            rook.set_pos([new_x, y])
            board.add_piece(self)
            board.add_piece(rook)
            return True
        return False  # Castling didn't work

    def set_check(self, check):
        """
        Setter for check flag

        :param check: Value to set to the flag
        """
        self.checked = check

    def valid_moves(self, board):
        moves = []
        validmoves = []
        x, y = self.get_pos()

        # Normal moves
        for tx in range(x-1, x+2):
            if tx in range(0, 8):
                for ty in range(y-1, y+2):
                    if ty in range(0, 8):
                        if not (tx == x and ty == y):
                            moves.append([tx, ty])

        # Castling
        if self.can_castle():
            for tx in range(x-1, -1, -1):
                square = board.get_square([tx, y])
                if square != 0:
                    if isinstance(square, Rook) and square.can_castle():  # Check whether it's the final square
                        moves.append([x-2, y])
                    else:
                        break
            for tx in range(x+1, 8, 1):
                square = board.get_square([tx, y])
                if square != 0:
                    if isinstance(square, Rook) and square.can_castle():
                        moves.append([x+2, y])
                    else:
                        break

        for move in moves:
            if self.is_valid(self.color, move, board):
                validmoves.append(move)

        return validmoves

    def get_checked(self):
        """
        Getter for check flag

        :return: Returns king's checked flag
        """
        return self.checked

    def is_checked(self, board):
        """
        Checks if king is in check by any other piece

        :param board: Board the game is running on
        :return: True if it's being checked
        """
        x, y = self.get_pos()
        if self.get_color() == "w":
            mod = 1
        else:
            mod = -1
        # Check Bishop + Queen diagonal
        for pos in self.check_diagonal(board):
            square = board.get_square(pos)
            if isinstance(square, (Bishop, Queen)) and square.get_color() != self.get_color():
                return True
        # Check Rook + Queen line
        for pos in self.check_perpendicular(board):
            square = board.get_square(pos)
            if isinstance(square, (Rook, Queen)) and square.get_color() != self.get_color():
                return True
        # Check Knight
        for pos in self.get_knight_moves(board):
            square = board.get_square(pos)
            if isinstance(square, Knight):
                if square.get_color() != self.get_color():
                    return True
        # Check opposing King
        for tx in range(x-1, x+2, 1):
            if tx in range(8):
                for ty in range(y-1, y+2, 1):
                    if ty in range(8):
                        if not(tx == x and ty == y):
                            square = board.get_square([tx, ty])
                            if isinstance(square, King):
                                return True
        # Check for pawns
        for tx in [x-1, x+1]:
            if tx in range(8) and y+mod in range(8):
                square = board.get_square([tx, y + mod])
                if isinstance(square, Pawn):
                    if square.get_color() != self.get_color():
                        return True
        return False

    def get_knight_moves(self, board):
        """
        Returns all possible squares a knight can move to, relative to current position

        :param board: Board the game is playing on
        :return: A list of positions
        """
        moves = []
        x, y = self.get_pos()
        # Far left and far right moves
        for ty in [y - 1, y + 1]:
            for tx in [x + 2, x - 2]:
                if board.get_square([tx, ty]) != 0:
                    moves.append([tx, ty])
        # top right and top left moves
        for ty in [y - 2, y + 2]:
            for tx in [x + 1, x - 1]:
                if board.get_square([tx, ty]) != 0:
                    moves.append([tx, ty])
        return moves

    def check_diagonal(self, board):
        moves = []
        x, y = self.get_pos()
        ran = range(8)
        # UP RIGHT
        temp_x = x + 1
        temp_y = y + 1

        while temp_x in ran and temp_y in ran:
            square = board.get_square([temp_x, temp_y])
            if square != 0:
                moves.append([temp_x, temp_y])
                break
            else:
                temp_x = temp_x + 1
                temp_y = temp_y + 1

        # DOWN RIGHT

        temp_x = x + 1
        temp_y = y - 1

        while temp_x in ran and temp_y in ran:
            square = board.get_square([temp_x, temp_y])
            if square != 0:
                moves.append([temp_x, temp_y])
                break
            else:
                temp_x = temp_x + 1
                temp_y = temp_y - 1
        # DOWN LEFT

        temp_x = x - 1
        temp_y = y - 1

        while temp_x in ran and temp_y in ran:
            square = board.get_square([temp_x, temp_y])
            if square != 0:
                moves.append([temp_x, temp_y])
                break
            else:
                temp_x = temp_x - 1
                temp_y = temp_y - 1
        # UP LEFT

        temp_x = x - 1
        temp_y = y + 1

        while temp_x in ran and temp_y in ran:
            square = board.get_square([temp_x, temp_y])
            if square != 0:
                moves.append([temp_x, temp_y])
                break
            else:
                temp_x -= 1
                temp_y += 1
        return moves

    def check_perpendicular(self, board):
        moves = []
        x, y = self.get_pos()

        # Check left
        for tx in range(self.pos[0] - 1, -1, -1):
            square = board.get_square([tx, y])
            if square != 0:
                moves.append([tx, y])
                break

        # Check right

        for tx in range(self.pos[0] + 1, 8, 1):
            square = board.get_square([tx, y])
            if square != 0:
                moves.append([tx, y])
                break

        # Check up
        for ty in range(self.pos[1] + 1, 8, 1):
            square = board.get_square([x, ty])
            if square != 0:
                moves.append([x, ty])
                break

        # Check up
        for ty in range(self.pos[1] - 1, -1, -1):
            square = board.get_square([x, ty])
            if square != 0:
                moves.append([x, ty])
                break

        return moves

    def can_castle(self):
        """
        Getter for castling flag

         :return: True if can castle
        """
        return self.castleable

    def flag_uncastleable(self):
        """
        Sets castling flag to False
        """
        self.castleable = False

    def get_copy(self):
        return King(self.pos, self.color, self.can_castle(), self.get_checked())


class Knight (Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_knight
        else:
            self.img = w_knight

    def __str__(self):
        return "N"

    def valid_moves(self, board):
        moves = []
        x, y = self.get_pos()

        # Far left and far right moves
        for ty in [y-1, y+1]:
            for tx in [x+2, x-2]:
                if self.is_valid(self.get_color(), [tx, ty], board):
                    moves.append([tx, ty])
        # top right and top left moves
        for ty in [y-2, y+2]:
            for tx in [x+1, x-1]:
                if self.is_valid(self.get_color(), [tx, ty], board):
                    moves.append([tx, ty])
        return moves

    def get_copy(self):
        return Knight(self.pos, self.color)


class Pawn (Piece):

    def __init__(self, pos, color, passant=False):
        Piece.__init__(self, pos, color)
        self.passant = passant  # Flag for en passant moves against the piece
        if color == "b":
            self.img = b_pawn
        else:
            self.img = w_pawn

    def __str__(self):
        return "P"

    def is_taking(self, board, move):
        if board.get_square(move) == 0:
            if self.get_pos()[0] != move[0]:  # En passant
                return True
            return False
        return True

    def get_passant(self):
        """
        Getter for en passant flag

        :return: True if can be taken en passant
        """
        return self.passant

    def clear_passant(self):
        """
        Sets en passant flag to false
        """
        self.passant = False

    def move(self, pos, board):
        if pos[1] in [0, 7]:
            piece = Queen(pos, self.color)
            board.add_piece(piece)
            board.add_blank(self.pos)
            return True
        else:
            x, y = self.get_pos()
            if y != pos[1]:  # Taking a piece
                square = board.get_square(pos)
                if square == 0:  # En Passant
                    board.add_blank([pos[0], y])
            if abs(y - pos[1]) == 2:
                self.passant = True
            board.add_blank([x, y])
            self.pos = pos
            board.add_piece(self)
            return True

    def is_valid(self, color, move, board):
        if not (move[0] in range(0, 8) and move[1] in range(0, 8)):
            return False
        square = board.get_square(move)
        x = move[0]

        if x == self.pos[0]:  # Moving forward
            if square == 0:
                if board.test_move(self.pos, move):
                    return True
        else:  # Taking a piece
            if isinstance(square, Piece) and square.get_color() != self.color:
                if board.test_move(self.pos, move):
                    return True
        return False

    def valid_moves(self, board):
        moves = []
        validmoves = []
        x, y = self.get_pos()
        mod = 1  # 1 for white, -1 for black
        if self.get_color() == "b":
            mod = -1
        if (y == 1 and mod == 1) or (y == 6 and mod == -1):
            moves.append([x, y+(mod * 2)])
        for tx in range(x-1, x+2, 1):
            moves.append([tx, y + mod])
        for move in moves:
            if self.is_valid(self.color, move, board):
                validmoves.append(move)
        # Check for en passant captures
        if x > 0:
            square = board.get_square([x - 1, y])
            if self.check_passant(square):
                if board.get_square([x - 1, y + mod]) == 0:
                    if board.test_move(self.get_pos(), [x-1, y+mod]):
                        validmoves.append([x - 1, y + mod])
        if x < 7:
            square = board.get_square([x + 1, y])
            if self.check_passant(square):
                if board.get_square([x + 1, y + mod]) == 0:
                    if board.test_move(self.get_pos(), [x - 1, y + mod]):
                        validmoves.append([x + 1, y + mod])

        return validmoves

    def check_passant(self, square):
        """
        Returns true if there is an en passant able pawn on the specified position

        :param square: Square to check
        :return: True if en passant flag at that position is True
        """
        if square == 0:
            return False
        if isinstance(square, Pawn) and square.get_color() != self.color:
            if square.get_passant():
                return True

    def get_copy(self):
        return Pawn(self.pos, self.color, self.get_passant())


class Queen (Piece):
    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_queen
        else:
            self.img = w_queen

    def __str__(self):
        return "Q"

    def valid_moves(self, board):
        moves = self.check_diagonal(board)
        for move in self.check_perpendicular(board):
            moves.append(move)
        return moves

    def get_copy(self):
        return Queen(self.pos, self.color)


class Rook (Piece):
    def __init__(self, pos, color, cast=True):
        Piece.__init__(self, pos, color)
        if color == "b":
            self.img = b_rook
        else:
            self.img = w_rook
        self.castleable = cast

    def __str__(self):
        return "R"

    def move(self, pos, board):
        x, y = self.get_pos()
        board.add_blank([x, y])
        self.pos = pos
        board.add_piece(self)
        if self.can_castle():
            self.flag_uncastleable()
        return True

    def can_castle(self):
        """
        Getter for castling flag

         :return: True if can castle
        """
        return self.castleable

    def flag_uncastleable(self):
        """
        Sets castling flag to False
        """
        self.castleable = False

    def valid_moves(self, board):
        moves = self.check_perpendicular(board)
        return moves

    def get_copy(self):
        return Rook(self.pos, self.color, self.can_castle())
