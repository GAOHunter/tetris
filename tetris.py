import os, sys
import pygame
from pygame.locals import *

from game_utility import *
from board import Board
from block import Block, Mino

SCREEN_SIZE = 500, 800

# TODO: fix bugs with line clearing(should be good), hard drop (when you pass the highest)
# TODO: add game over
# TODO: add score, clock, up next queue, holds, pictures
# TODO: fix rotation stuff
# TODO: problems with keyboard input
# TODO: clean and organize code
# TODO: colors

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("TETRIS")

    clock = pygame.time.Clock()
    time = 0
    timeLimit = 2000 #2000 milliseconds = 2 seconds
    dropOne = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    tetrisLogo, _ = load_image("tetrislogo.jpg")


    board = Board()
    boardPanel = pygame.sprite.Group(board)
    upNextList = [Mino(board) for x in range(3)]
    heldMino = None
    newMino = True

    while 1:
        clock.tick()
        time += clock.get_time()

        if newMino:
            mino = upNextList.pop(0)
            mino.activate()
            upNextList.append(Mino(board))
            for i in range(3):
                upNextList[i].updateBlocks(x = 13, y = 5 +(5*i))
                upNextList[i].blockGroup.update()
            newMino = False

        if time >= timeLimit:
            dropOne = True
            time = 0

        moveDir = None
        rotateDir = None
        hardDrop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_ESCAPE]:
                    return
                if keys[K_c]:
                    if heldMino != None:
                        temp = mino
                        mino = heldMino
                        heldMino = temp
                        heldMino.deactivate()
                        heldMino.blockGroup.update()
                        mino.activate()
                    else:
                        heldMino = mino
                        heldMino.deactivate()
                        heldMino.blockGroup.update()
                        mino = upNextList.pop(0)
                        upNextList.append(Mino(board))
                        for i in range(3):
                            upNextList[i].updateBlocks(x = 13, y = 5 +(5*i))
                            upNextList[i].blockGroup.update()
                        mino.activate()
                if keys[K_DOWN]:
                    hardDrop = True
                elif keys[K_UP]:
                    moveDir = DOWN
                elif keys[K_RIGHT]:
                    moveDir = RIGHT
                elif keys[K_LEFT]:
                    moveDir = LEFT
                if keys[K_x]:
                    rotateDir = COUNTERCLOCK #TODO: fix the rotation mechanics
                elif keys[K_z]:
                    rotateDir = CLOCK

        newMino = mino.updateMino(hardDrop, dropOne, moveDir, rotateDir)
        if dropOne:
            dropOne = False

        mino.blockGroup.update()
        board.clearLines()

        screen.blit(background, (0, 0))
        screen.blit(tetrisLogo, (125, 25))
        boardPanel.draw(screen)
        for upNextMino in upNextList:
            upNextMino.blockGroup.draw(screen)
        if heldMino != None:
            heldMino.blockGroup.draw(screen)
        board.blockGroup.draw(screen)
        mino.blockGroup.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()
