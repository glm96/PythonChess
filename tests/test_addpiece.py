import Board
import Piece


def test_addpiece():
    board = Board.Board()
    pos = [3, 4]
    wq = Piece.Queen(pos, "w")
    board.add_piece(wq)
    assert board.get_square(pos) is wq
