import os, sys
import pygame
from pygame.locals import *
from game_utility import *

class Board(pygame.sprite.Sprite):
    """ The tetris board. """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("grid.gif")
        self.rect = (100, 100) #need these to not be literal, use a var
        self.width = 10
        self.height = 20
        #self.cellArr = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]

    #def checkLines(self):

    #def clearLines(self):
