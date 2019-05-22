import Board
import Piece


def test_en_passant_1():
    board = Board.Board()

    # Kings are needed for check testing when calling valid_moves
    wk = Piece.King([7, 7], "w")
    bk = Piece.King([0, 7], "b")
    board.add_piece(wk)
    board.add_piece(bk)

    wp = Piece.Pawn([2, 1], "w")
    bp = Piece.Pawn([3, 3], "b")
    board.add_piece(wp)
    board.add_piece(bp)
    wp.move([2, 3], board)
    assert [2, 2] in bp.valid_moves(board)


def test_en_passant_2():
    board = Board.Board()

    # Kings are needed for check testing when calling valid_moves
    wk = Piece.King([7, 7], "w")
    bk = Piece.King([0, 7], "b")
    board.add_piece(wk)
    board.add_piece(bk)

    wp = Piece.Pawn([2, 1], "w")
    bp = Piece.Pawn([3, 3], "b")
    board.add_piece(wp)
    board.add_piece(bp)
    wp.move([2, 3], board)
    wp.clear_passant()  # Clear en passant flag so it can't be taken that way
    assert not [2, 2] in bp.valid_moves(board)


test_en_passant_1()
test_en_passant_2()