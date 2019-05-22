import Board
import Piece

def test_addblank():
    board = Board.Board()
    board.load_board()  # Fills the board with standard game pieces
    assert isinstance(board.get_square([0, 0]), Piece.Rook)
    board.add_blank([0, 0])
    assert board.get_square([0, 0]) == 0
