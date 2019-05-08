import pygame
from Board import Board
from Piece import Bishop


boardimg = pygame.image.load("imgs\\board.png")



width = 500
height = 500
white = (255,255,255)
origin = (0,0)


def main():

    board = Board()
    board.printBoard()

    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    done = False
    p = Bishop([3,3], "w")
    p.validMoves(board)
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(white)
        screen.blit(boardimg, origin)
        p.draw(screen)
        pygame.display.flip()
        clock.tick(50)

main()