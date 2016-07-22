import os, sys
import pygame
import random
from pygame.locals import *
from game_utility import *

class Mino():
    """A tetrimino. """
    def __init__(self):
        self.blocknum = random.randrange(1,8)
        if self.blocknum == I_MINO:
            self.rotationList = [[(0,2),(0,1),(0,0),(0,-1)],
                                [(2,0),(1,0),(0,0),(-1,0)],
                                [(0,1),(0,0),(0,-1),(0,-2)],
                                [(1,0),(0,0),(-1,0),(-2,0)]]
        elif self.blocknum == O_MINO:
            self.rotationList = [[(0,0),(0,1),(1,0),(1,1)],
                                [(0,0),(0,1),(1,0),(1,1)],
                                [(0,0),(0,1),(1,0),(1,1)],
                                [(0,0),(0,1),(1,0),(1,1)]]
        elif self.blocknum == T_MINO:
            self.rotationList = [[(-1,0),(0,0),(1,0),(0,-1)],
                                [(0,1),(0,0),(0,-1),(-1,0)],
                                [(1,0),(0,0),(-1,0),(0,1)],
                                [(0,-1),(0,0),(0,1),(1,0)]]
        elif self.blocknum == J_MINO:
            self.rotationList = [[(-1,0),(0,0),(0,1),(0,2)],
                                [(0,1),(0,0),(1,0),(2,0)],
                                [(1,0),(0,0),(0,-1),(0,-2)],
                                [(0,-1),(0,0),(-1,0),(-2,0)]]
        elif self.blocknum == L_MINO:
            self.rotationList = [[(1,0),(0,0),(0,1),(0,2)],
                                [(0,-1),(0,0),(1,0),(2,0)],
                                [(-1,0),(0,0),(0,-1),(0,-2)],
                                [(0,1),(0,0),(-1,0),(-2,0)]]
        elif self.blocknum == S_MINO:
            self.rotationList = [[(-1,0),(0,0),(0,1),(1,1)],
                                [(0,1),(0,0),(1,0),(1,-1)],
                                [(1,0),(0,0),(0,-1),(-1,-1)],
                                [(0,-1),(0,0),(-1,0),(-1,1)]]
        elif self.blocknum == Z_MINO:
            self.rotationList = [[(1,0),(0,0),(0,1),(-1,1)],
                                [(0,-1),(0,0),(1,0),(1,1)],
                                [(1,0),(0,0),(0,-1),(1,-1)],
                                [(0,1),(0,0),(-1,0),(-1,-1)]]
        else:
            print "Somehthing has gone terribly wrong."
            self.rotationList = None
        self.rotation = 0
        self.x = 5
        self.y = 2
        self.blockGroup = pygame.sprite.Group()
        self.blockList = []
        for i in range(0,4):
            block = Block(self.blocknum)
            (dx, dy) = self.rotationList[self.rotation][i]
            block.rect = (25*(self.x+dx)+100,25*(self.y+dy)+100)
            self.blockList.append(block)
            self.blockGroup.add(block)

    def updateBlocks(self, x = None, y = None):
        for i in range(0, 4):
            if x != None:
                self.x = x
            if y!= None:
                self.y = y
            (dx, dy) = self.rotationList[self.rotation][i]
            self.blockList[i].rect = (25*(self.x+dx)+100,25*(self.y+dy)+100)
        #starting numbers here should not be literal, use a var

    def moveMino(self, direction):
        if direction == DOWN:
            self.updateBlocks(x = None, y = self.y+1)
        elif direction == RIGHT:
            self.updateBlocks(x = self.x+1, y = None)
        elif direction == LEFT:
            self.updateBlocks(x = self.x-1, y = None)

    def rotateMino(self, direction):
        curr = self.rotation
        if direction == CLOCK:
            if curr <= 2:
                self.rotation = curr + 1
            else:
                self.rotation = 0
        elif direction == COUNTERCLOCK:
            if curr >= 1:
                self.rotation = curr - 1
            else:
                self.rotation = 3
        self.updateBlocks()

class Block(pygame.sprite.Sprite):
    """A tetrimino block. """
    def __init__(self, blocknum):
        pygame.sprite.Sprite.__init__(self)
        blockstr = "block" + str(blocknum) + ".png"
        self.image, self.rect = load_image(blockstr)
