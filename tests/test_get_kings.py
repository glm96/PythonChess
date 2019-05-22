import Board
import Piece


def test_get_kings():
    board = Board.Board()
    board.load_board()
    w_king, b_king = board.get_kings()
    assert isinstance(w_king, Piece.King) and isinstance(b_king, Piece.King)


test_get_kings()
