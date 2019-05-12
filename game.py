from Board import Board
from Piece import *

boardimg = pygame.image.load("img\\board.png")
windowicon = pygame.image.load("img\\icon.png")

width = 500
height = 500
white = (255, 255, 255)
red = pygame.Color.r
origin = (0, 0)
clicked = False
clickedPiece = 0
lastMoved = 0
wturn = True

board = Board()


def main():

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PyChess")
    pygame.display.set_icon(windowicon)
    clock = pygame.time.Clock()
    done = False
    board.load_board()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                on_click_board(event)
        screen.fill(white)
        screen.blit(boardimg, origin)
        board.update(screen)
        if isinstance(clickedPiece, Piece):
            for move in clickedPiece.valid_moves(board):
                highlight_square(move, screen)
        pygame.display.flip()
        clock.tick(50)


def format_pos(pos):
    x = chr(ord('A')+pos[0])
    return x + str(pos[1])


def on_click_board(event):
    global clicked, clickedPiece, wturn, lastMoved
    side = width / 8
    x = int(event.pos[0] / side)
    y = int((event.pos[1] - 500) * -1 / side)
    if wturn:
        turn = "w"
    else:
        turn = "b"
    square = board.get_square([x, y])
    if not clicked:
        if square != 0:
            if square.get_color() == turn:
                clickedPiece = square
                clicked = True
    else:
        if [x, y] in clickedPiece.valid_moves(board):
            if clickedPiece.move([x, y], board):
                wturn = not wturn
                clear_passants()
                lastMoved = clickedPiece
        clicked = False
        clickedPiece = 0


def highlight_square(pos, screen):
    x = int(width / 8 * pos[0] + width/16)
    y = int(height - height / 8 * (1 + pos[1]) + height/16)
    pygame.draw.circle(screen, (255, 0, 0), [x, y],  8, 0)


def clear_passants():
    if isinstance(lastMoved, Pawn):
        lastMoved.clear_passant()


main()
