from Piece import *


class Board:
    def __init__(self, board=None):
        self.rows = 8
        if board is None:
            self.board = [[0 for _ in range(self.rows)]for _ in range(self.rows)]
        else:
            self.board = board

    def update(self, screen):
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, King):
                    square.set_check(square.is_checked(self))
                if isinstance(square, Piece):
                    square.draw(screen)

    def get_kings(self):
        kings = []
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, King):
                    kings.append(square)
        return kings

    def print_board(self):
        for j in range(self.rows-1, -1, -1):
            for i in range(self.rows):
                print(self.board[i][j], end='')
            print("")

    def can_team_move(self, color):

        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, Piece):
                    if square.get_color() == color:
                        if len(square.valid_moves(self)) != 0:
                            return True
        return False

    def get_square(self, pos):
        x, y = pos
        if x in range(8) and y in range(8):
            return self.board[x][y]
        return 0

    def load_board(self):

        # Pawns
        for x in range(8):
            wpawn = Pawn([x, 1], "w")
            bpawn = Pawn([x, 6], "b")
            self.add_piece(wpawn)
            self.add_piece(bpawn)

        # White pieces
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
        x, y = piece.get_pos()
        self.board[x][y] = piece

    def add_blank(self, pos):
        if pos[0] in range(8) and pos[1] in range(8):
            self.board[pos[0]][pos[1]] = 0

    def get_board_copy(self):
        board = [[0 for _ in range(self.rows)] for _ in range(self.rows)]
        for x in range(8):
            for y in range(8):
                square = self.get_square([x, y])
                if isinstance(square, Piece):
                    board[x][y] = square.get_copy()
        return board

    def test_move(self, origin, dest):  # Returns true if move is valid
        testboard = Board(self.get_board_copy())
        square = testboard.get_square(origin)
        testboard.add_blank(origin)
        square.set_pos(dest)
        testboard.add_piece(square)
        color = square.get_color()
        for x in range(8):
            for y in range(8):
                square = testboard.get_square([x, y])
                if isinstance(square, King) and square.get_color() == color:
                    king = square
                    if king.is_checked(testboard):
                        return False
        return True
