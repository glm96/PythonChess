from Board import Board
from Piece import *
import re

boardimg = pygame.image.load("img\\board.png")
windowicon = pygame.image.load("img\\icon.png")

width = 500
height = 500
white = (255,255,255)
red = pygame.Color.r
origin = (0,0)
clicked = False
clickedPiece = 0
lastMoved = 0
wturn = True

board = Board()


def main():

    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("PyChess")
    pygame.display.set_icon(windowicon)
    clock = pygame.time.Clock()
    done = False
    board.loadBoard()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                onClickBoard(event)
        screen.fill(white)
        screen.blit(boardimg, origin)
        board.update(screen)
        if clickedPiece != 0:
            for move in clickedPiece.validMoves(board):
                highlightSquare(move, screen)
        pygame.display.flip()
        clock.tick(50)


def formatPos(pos):
    x = chr(ord('A')+pos[0])
    return x + str(pos[1])


def onClickBoard(event):
    global clicked, clickedPiece, wturn, lastMoved
    side = width / 8
    x = int(event.pos[0] / side)
    y = int((event.pos[1] - 500) * -1 / side)
    if wturn:
        turn = "w"
    else:
        turn = "b"
    square = board.getSquare([x, y])
    if not clicked:
        if square != 0:
            if square.getColor() == turn:
                clickedPiece = square
                clicked = True
    else:
        if clickedPiece.move([x, y], board):
            wturn = not wturn
            clearPassants()
            lastMoved = clickedPiece
        clicked = False
        clickedPiece = 0


def highlightSquare(pos, screen):
    x = int(width / 8 * pos[0] + width/16)
    y = int(height - height / 8 * (1 + pos[1]) + height/16)
    pygame.draw.circle(screen, (255,0,0), [x, y],  8, 0)


def clearPassants():
    if lastMoved != 0:
        regex = ".P"
        if re.search(regex, str(lastMoved)):
            lastMoved.clearPassant()


main()