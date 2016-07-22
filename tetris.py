import os, sys
import pygame
from pygame.locals import *

from game_utility import *
from board import Board
from block import Block, Mino

SCREEN_SIZE = 500, 800

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("TETRIS")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    board = Board()
    boardPanel = pygame.sprite.Group(board)
    mino = Mino()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[K_DOWN]:
                mino.moveMino(DOWN)
            elif keys[K_RIGHT]:
                mino.moveMino(RIGHT)
            elif keys[K_LEFT]:
                mino.moveMino(LEFT)
            elif keys[K_z]:
                mino.rotateMino(COUNTERCLOCK)
            elif keys[K_x]:
                mino.rotateMino(CLOCK)

        mino.blockGroup.update()

        screen.blit(background, (0, 0))
        boardPanel.draw(screen)
        mino.blockGroup.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()
