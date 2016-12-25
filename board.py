import os, sys
import pygame
from pygame.locals import *
from game_utility import *

class Board(pygame.sprite.Sprite):
    """ The tetris board. """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("grid.gif")
        self.rect = (BOARD_X, BOARD_Y) #need these to not be literal, use a var
        self.width = 10
        self.height = 20
        self.blockGroup = pygame.sprite.Group()
        self.blockMatrix = [[False for x in range(self.width)] for y in range(self.height)]
        self.highestList = [20]*10

    def clearLines(self):
        for line in self.blockMatrix:
            lineComplete = True
            for block in line:
                if block == False:
                    lineComplete = False
            if lineComplete:
                self.updateBlocks(self.blockMatrix.index(line))
                self.blockMatrix.remove(line)
                newLine = [False]*10
                self.blockMatrix.insert(0, newLine)
                for block in line:
                    self.blockGroup.remove(block)
        self.findHighest()

    def updateBlocks(self, lineNumber):
        for i in range(0, lineNumber):
            line = self.blockMatrix[i]
            for block in line:
                if block != False:
                    block.y += 1
                    block.rect = (25*block.x+BOARD_X,25*block.y+BOARD_Y)

    def findHighest(self):
        self.highestList = [20]*10
        for line in reversed(self.blockMatrix):
            for block in line:
                if block != False:
                    self.highestList[block.x] = block.y
