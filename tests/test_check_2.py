import Piece
import Board


def test_check_2(): # Not checked
    board = Board.Board()
    wk = Piece.King([4, 3], "w")
    br = Piece.Rook([3, 4], "b")
    board.add_piece(wk)
    board.add_piece(br)
    assert not wk.is_checked(board)