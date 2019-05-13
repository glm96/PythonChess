from Board import Board
from Piece import *
import easygui

boardimg = pygame.image.load("img\\board.png")
windowicon = pygame.image.load("img\\icon.png")

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
turn = "w"
msg = ""
board = Board()


def main():

    global w_king, b_king
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PyChess")
    pygame.display.set_icon(windowicon)
    clock = pygame.time.Clock()
    done = False
    board.load_board()
    kings = board.get_kings()
    if kings[0].get_color() == "w":  # Will always be true in standard games
        w_king = kings[0]
        b_king = kings[1]
    else:
        w_king = kings[1]
        b_king = kings[0]

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


def game_restart():
    global game_ended, lastMoved, clicked, turn, w_king, b_king
    for x in range(8):
        for y in range(8):
            board.add_blank([x, y])
    board.load_board()
    kings = board.get_kings()
    if kings[0].get_color() == "w":  # Will always be true in standard games
        w_king = kings[0]
        b_king = kings[1]
    else:
        w_king = kings[1]
        b_king = kings[0]
    game_ended = False
    lastMoved = 0
    clicked = False
    turn = "w"


def format_pos(pos):
    x = chr(ord('A')+pos[0])
    return x + str(pos[1])


def on_click_board(event):
    global clicked, clickedPiece, turn, lastMoved, game_ended, msg
    side = width / 8
    x = int(event.pos[0] / side)
    y = int((event.pos[1] - 500) * -1 / side)
    if not game_ended:
        square = board.get_square([x, y])
        if not clicked:  # Selecting a piece
            if square != 0:
                if square.get_color() == turn:
                    clickedPiece = square
                    clicked = True
        else:  # Piece was selected, discard or try to move
            if [x, y] in clickedPiece.valid_moves(board):
                if clickedPiece.move([x, y], board):
                    if turn == "w":
                        turn = "b"
                    else:
                        turn = "w"
                    clear_passants()
                    lastMoved = clickedPiece
            clicked = False
            clickedPiece = 0
            if not board.can_team_move(turn):
                game_ended = True
                lastMoved = 0
                if turn == "w":
                    if w_king.is_checked(board):
                        msg = "Black Wins"
                    else:
                        msg = "Draw"
                else:
                    if turn == "b":
                        if b_king.is_checked(board):
                            msg = "White Wins"
                        else:
                            msg = "Draw"
    else:  # Game has ended, ask for restart
        pass


def highlight_square(pos, screen):
    x = int(width / 8 * pos[0] + width/16)
    y = int(height - height / 8 * (1 + pos[1]) + height/16)
    pygame.draw.circle(screen, (255, 0, 0), [x, y],  8, 0)


def clear_passants():
    if isinstance(lastMoved, Pawn):
        lastMoved.clear_passant()


main()
