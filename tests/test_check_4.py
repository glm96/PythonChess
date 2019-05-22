import Board
import Piece

def test_check_4():  # Checked by pawn
    board = Board.Board()
    wk = Piece.King([4, 3], "w")
    bp = Piece.Pawn([5, 4], "b")
    board.add_piece(wk)
    board.add_piece(bp)
    assert wk.is_checked(board)