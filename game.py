from Board import Board
from Piece import *
import easygui
import datetime
import pymongo

boardimg = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\board.png")
windowicon = pygame.image.load("C:\\Users\\tyrio\\PycharmProjects\\PythonChess\\img\\icon.png")

WHITE = "w"
BLACK = "b"
width = 500
height = 500
checker = width/8
white = (255, 255, 255)
red = pygame.Color.r
origin = (0, 0)
clicked = False
game_ended = False
clickedPiece = 0
lastMoved = 0
turn = WHITE
msg = ""
PGN = ""
n_turn = 1
PGN_result = ""
board = Board()


def main():

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PyChess")
    pygame.display.set_icon(windowicon)
    clock = pygame.time.Clock()
    done = False
    board.load_board()
    store_kings()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                on_click_board(event)
        screen.fill(white)
        screen.blit(boardimg, origin)
        board.update(screen)
        if not game_ended:
            if isinstance(clickedPiece, Piece):
                for move in clickedPiece.valid_moves(board):
                    highlight_square(move, screen)
        else:  # Draw rect
            pygame.display.flip()
            choice = easygui.buttonbox(msg, 'Restart?', ['Restart', 'Quit'])
            if choice == 'Restart':
                game_restart()
            else:
                done = True
        pygame.display.flip()
        clock.tick(50)


def store_kings():
    """
    Saves both King Objects to their respective variables, in order
    to quickly locate them in other functions.
    """

    global b_king, w_king
    kings = board.get_kings()
    if kings[0].get_color() == WHITE:  # Will always be true in standard games
        w_king = kings[0]
        b_king = kings[1]
    else:
        w_king = kings[1]
        b_king = kings[0]


def game_restart():
    """
    Starts a common game, setting pieces in place and clearing all the configurations used
    in last game
    """
    global game_ended, lastMoved, clicked, turn, w_king, b_king, PGN, PGN_result
    for x in range(8):
        for y in range(8):
            board.add_blank([x, y])
    board.load_board()
    store_kings()
    game_ended = False
    lastMoved = 0
    clicked = False
    turn = "w"
    PGN = ""
    PGN_result = ""


def format_pos(pos):
    """
    Return the position as letter+number coordinates, rather than two numbers, for PGN purposes

    :type pos: list
    :param pos: Position to be formated
    :return: Position in chess notation
    """
    x = chr(ord('a')+pos[0])
    return x + str(pos[1]+1)


def on_click_board(event):
    """
    Handler for clicks on the board

    Takes care of most of the game logic, checking whether the move was valid or not,
     then modifying global game variables however needed.

    :param event: Click event
    :return:
    """
    global clicked, clickedPiece, turn, lastMoved, game_ended, msg, PGN, PGN_result
    side = width / 8
    # Getting the click coordinates out of the event
    x = int(event.pos[0] / side)
    y = int((event.pos[1] - 500) * -1 / side)

    # Logic for in progress games
    if not game_ended:
        if not clicked:  # Selecting a piece
            square = board.get_square([x, y])
            if square != 0:
                if square.get_color() == turn:
                    clickedPiece = square
                    clicked = True
        else:  # Piece was selected, discard or try to move
            if [x, y] in clickedPiece.valid_moves(board):
                update_PGN(clickedPiece, [x, y])
                clickedPiece.move([x, y], board)
                if turn == WHITE:
                    turn = BLACK
                else:
                    turn = WHITE
                clear_passants()
                lastMoved = clickedPiece
            clicked = False
            clickedPiece = 0
            # Check whether the game ended ith last move or not
            if not board.can_team_move(turn):
                PGN = PGN[0:len(PGN)-1]+"#"
                game_ended = True
                lastMoved = 0
                if turn == WHITE:
                    if w_king.is_checked(board):
                        msg = "Black Wins"
                        PGN_result = "0-1"
                    else:
                        msg = "Draw"
                        PGN_result = "1/2-1/2"
                else:
                    if turn == BLACK:
                        if b_king.is_checked(board):
                            msg = "White Wins"
                            PGN_result = "1-0"
                        else:
                            msg = "Draw"
                            PGN_result = "1/2-1/2"
                store_game()    # Store the game on the database
    else:  # Game has ended, currently asking for restart / exit
        pass


def update_PGN(piece, move):
    """
    Adds current move to PGN
    :type piece: Piece
    :param piece: Piece that moved
    :param move: Destination move
    :return: Returns true when stored
    """
    global n_turn, PGN
    s2 = ""
    s3 = ""
    s4 = ""
    if turn == WHITE:
        s = str(n_turn)+". "
    else:
        n_turn += 1
        s = ""

    #  Castling
    if isinstance(piece, King):
        if abs(move[0] - piece.get_pos()[0]) == 2:  # Castling
            if move[0] == 2:
                s2 = "O-O-O"
            else:
                s2 = "O-O"
            clickedPiece.move(move, board)
            res = s + s2 + " "
            if res == "":
                print(PGN)
            PGN += res
            return True

    #  Normal movements
    if not isinstance(piece, Pawn):
        if board.is_ambiguous(piece, move):
            s2 = str(piece)+format_pos(piece.get_pos())[0:1]
        else:
            s2 = str(piece)
    if piece.is_taking(board, move):
        s3 = "x"
        if isinstance(piece, Pawn):
            s2 = format_pos(piece.get_pos())[0:1]  # Pawns taking need column

    clickedPiece.move(move, board)  # make the move now to be able to check for checks

    #  Checks
    if piece.get_color() == WHITE:
        if b_king.is_checked(board):
            s4 = "+"
    else:
        if w_king.is_checked(board):
            s4 = "+"

    res = s+s2+s3+format_pos(move)+s4+" "
    if res == "":
        print(PGN)
    PGN += res
    return True


def store_game():
    """
    Stores the game to a local mongoDB database
    :return:
    """
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["pychess"]
    col = db["games"]

    now = datetime.datetime.now()
    res = {"Event": "Friendly PyChess game",
           "Site": "PyChess application",
           "Date": now.strftime("%Y.%m.%d"),
           "Round": "n/a",
           "White": "Player1",
           "Black": "Player2",
           "Result": PGN_result,
           "Game": PGN,
           "FEN": get_FEN()}
    col.insert_one(res)


def get_FEN():
    """
    Generates FEN string of current board

    :return: Returns a string with current board's FEN
    """
    cont = 0
    lines = []
    line = ""
    passant = "-"
    for y in range(7, -1, -1):
        for x in range(0, 8):
            square = board.get_square([x, y])
            if isinstance(square, Pawn):
                if square.get_passant():
                    passant = format_pos(square.get_pos())
            if isinstance(square, Piece):
                if cont > 0:
                    line += str(cont)
                    cont = 0
                line += square.get_FEN()
            else:
                cont += 1
                if x == 7:
                    line += str(cont)
                    cont = 0
        lines.append(line)
        line = ""
    boardfen = ""
    for line in lines:
        boardfen += line + "/"

    castling = " "
    # White castling availability
    if w_king.can_castle():
        w_square_kingside = board.get_square([7,0])
        w_square_queenside = board.get_square([0, 0])
        if isinstance(w_square_kingside, Rook):
            if w_square_kingside.can_castle():
                castling += "K"
        if isinstance(w_square_queenside, Rook):
            if w_square_queenside.can_castle():
                castling += "Q"
    # Black castling availability
    if b_king.can_castle():
        b_square_kingside = board.get_square([7, 7])
        b_square_queenside = board.get_square([0, 7])
        if isinstance(b_square_kingside, Rook):
            if b_square_kingside.can_castle():
                castling += "k"
        if isinstance(b_square_queenside, Rook):
            if b_square_queenside.can_castle():
                castling += "q"

    return boardfen + " " + turn + castling + " " + passant + " " + str(0) + " " + str(n_turn)


def highlight_square(pos, screen):
    """
    Draw circles on valid destination squares for current piece

    :type pos: list
    :param pos: Position to highlight
    :param screen: PyGame screen controller
    """
    x = int(width / 8 * pos[0] + width/16)
    y = int(height - height / 8 * (1 + pos[1]) + height/16)
    pygame.draw.circle(screen, (255, 0, 0), [x, y],  8, 0)


def clear_passants():
    """
    Clear en passant flag from last moved pawn
    """
    if isinstance(lastMoved, Pawn):
        lastMoved.clear_passant()


main()
