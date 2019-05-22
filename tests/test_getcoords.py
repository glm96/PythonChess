import Piece


def test_getcoords():
    width = Piece.width
    height = Piece.height
    assert Piece.Piece.get_coords([1, 0]) == (width/8, height-height/8)

def test_getcoords_tuple():
    width = Piece.width
    height = Piece.height
    assert Piece.Piece.get_coords((1, 0)) == (width/8, height-height/8)

test_getcoords()
test_getcoords_tuple()