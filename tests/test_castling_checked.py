import Board
import Piece


def test_castling_checked():
    board = Board.Board()

    # Kings are needed for check testing when calling valid_moves
    wk = Piece.King([4, 0], "w")
    bk = Piece.King([7, 7], "b")
    board.add_piece(wk)
    board.add_piece(bk)

    wr = Piece.Rook([7, 0], "w")
    br = Piece.Rook([4, 7], "b")
    board.add_piece(br)
    board.add_piece(wr)
    assert not [6, 0] in wk.valid_moves(board)

