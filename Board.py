from Piece import *


class Board:
    """
    Class representing the chess board, has information on current position of
    all pieces in the field, as well as other useful data
    """
    def __init__(self, board=None):
        """
        Board initializer. Can be called with a board parameter in order to replicate an specific board.

        :param board: 8x8 array with either a zero or a piece in each slot
        """
        self.rows = 8
        if board is None:
            self.board = [[0 for _ in range(self.rows)]for _ in range(self.rows)]
        else:
            self.board = board

    def update(self, screen):
        """
        Draw current board on the screen

        :param screen: PyGame screen controller
        """
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, King):
                    square.set_check(square.is_checked(self))
                if isinstance(square, Piece):
                    square.draw(screen)

    def get_kings(self):
        """
        Returns both king Piece objects

        :return: Array with both kings, with white being first
        """
        kings = []
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, King):
                    kings.append(square)
        return kings

    def print_board(self):
        """
        Prints current board to console for debugging purposes

        :return:
        """
        for j in range(self.rows-1, -1, -1):
            for i in range(self.rows):
                print(self.board[i][j], end='')
            print("")

    def can_team_move(self, color):
        """
        Checks whether a valid move exists or not for one of the players

        :param color: Color of the team being checked
        :return: True if it's possible to move, meaning game has not ended
        """
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, Piece):
                    if square.get_color() == color:
                        if len(square.valid_moves(self)) != 0:
                            return True
        return False

    def is_ambiguous(self, piece, move):
        """
        Checks whether two pieces of the same type can move to the same square in
        the same turn for PGN writing purposes

        :param piece: Piece that is trying to move to a square
        :param move: Destination square
        :return: True if another piece of the same type can move to the same square
        """
        color = piece.get_color()
        if isinstance(piece, (Rook, Knight)):  # Only these types can be ambiguous
            for x in range(8):
                for y in range(8):
                    square = self.get_square([x, y])
                    if (type(piece) is type(square))and square.get_color() == color:
                        if not (square is piece):
                            if move in square.valid_moves(self):
                                return True
        return False

    def get_square(self, pos):
        """
        Returns whatever is placed in the specified position

        :param pos: Position to check for
        :return: Stored piece or 0 if it's empty
        """
        x, y = pos
        if x in range(8) and y in range(8):
            return self.board[x][y]
        return 0

    def load_board(self):
        """
        Fill the board with pieces for a standard game
        """
        # Pawns
        for x in range(8):
            wpawn = Pawn([x, 1], "w")
            bpawn = Pawn([x, 6], "b")
            self.add_piece(wpawn)
            self.add_piece(bpawn)

        # # White pieces
        self.add_piece(Rook([0, 0], "w"))
        self.add_piece(Knight([1, 0], "w"))
        self.add_piece(Bishop([2, 0], "w"))
        self.add_piece(Queen([3, 0], "w"))
        self.add_piece(King([4, 0], "w"))
        self.add_piece(Bishop([5, 0], "w"))
        self.add_piece(Knight([6, 0], "w"))
        self.add_piece(Rook([7, 0], "w"))

        # Black pieces

        self.add_piece(Rook([0, 7], "b"))
        self.add_piece(Knight([1, 7], "b"))
        self.add_piece(Bishop([2, 7], "b"))
        self.add_piece(Queen([3, 7], "b"))
        self.add_piece(King([4, 7], "b"))
        self.add_piece(Bishop([5, 7], "b"))
        self.add_piece(Knight([6, 7], "b"))
        self.add_piece(Rook([7, 7], "b"))

    def add_piece(self, piece):
        """
        Adds the specified piece at its square

        :param piece: Piece object to place
        :return:
        """
        x, y = piece.get_pos()
        self.board[x][y] = piece

    def add_blank(self, pos):
        """
        Removes whatever piece was at the specified position

        :param pos: Piece to make empty
        """
        if pos[0] in range(8) and pos[1] in range(8):
            self.board[pos[0]][pos[1]] = 0

    def empty_board(self):
        """
        Fills the board with blanks
        """
        for x in range(8):
            for y in range(8):
                self.board[x][y] = 0

    def get_board_copy(self):
        """
        Returns an exact copy of the board with different instances of its pieces for testing moves

        :return: A Board type object with pieces in the same positions as self
        """
        board = [[0 for _ in range(self.rows)] for _ in range(self.rows)]
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, Piece):
                    board[x][y] = square.get_copy()
        return board

    def test_move(self, origin, dest, passant=False):
        """
        Method for testing whether a move is valid or not

        :param origin: Position of the piece to move
        :param dest: Destination of the moving piece
        :param passant: Flag for en passant takes, False by default
        :return: True if movement is valid
        """
        # Creating a copy of the board for testing the move
        testboard = Board(self.get_board_copy())
        square = testboard.get_square(origin)
        # Making testboard look like it would after the move
        testboard.add_blank(origin)
        if passant:
            testboard.add_blank([dest[0], origin[1]])  # Pawn to be taken
        square.set_pos(dest)
        testboard.add_piece(square)
        color = square.get_color()
        # Check if its own king got checked because of the move
        if color == "w":
            king = testboard.get_kings()[0]
        else:
            king = testboard.get_kings()[1]
        if king.is_checked(testboard):
            return False
        return True
