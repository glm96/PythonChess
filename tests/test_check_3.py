import Board
import Piece


def test_check_3():  # Checked by bishop
    board = Board.Board()
    wk = Piece.King([4, 3], "w")
    bb = Piece.Bishop([5, 4], "b")
    board.add_piece(wk)
    board.add_piece(bb)
    assert wk.is_checked(board)