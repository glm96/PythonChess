import Board
import Piece


def test_check_1():  # Checked by rook
    board = Board.Board()
    wk = Piece.King([4, 3], "w")
    br = Piece.Rook([2, 3], "b")
    board.add_piece(wk)
    board.add_piece(br)
    assert wk.is_checked(board)

