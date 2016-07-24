import os, sys
import pygame
import random
from pygame.locals import *
from game_utility import *


class Mino():
    """A tetrimino. """
    def __init__(self, board, blocknum = None):
        self.board = board
        if blocknum != None: #use this for testing specific pieces, take it out eventually
            self.blocknum = blocknum
        else:
            self.blocknum = random.randrange(1,8)
        if self.blocknum == I_MINO:
            self.rotationList = [[(2,0),(1,0),(0,0),(-1,0)],
                                [(0,1),(0,0),(0,-1),(0,-2)],
                                [(2,0),(1,0),(0,0),(-1,0)],
                                [(1,1),(1,0),(1,-1),(1,-2)]]
        elif self.blocknum == O_MINO:
            self.rotationList = [[(0,0),(0,1),(1,0),(1,1)],
                                [(0,0),(0,1),(1,0),(1,1)],
                                [(0,0),(0,1),(1,0),(1,1)],
                                [(0,0),(0,1),(1,0),(1,1)]]
        elif self.blocknum == T_MINO:
            self.rotationList = [[(1,0),(0,0),(-1,0),(0,1)],
                                [(0,-1),(0,0),(0,1),(1,0)],
                                [(-1,0),(0,0),(1,0),(0,-1)],
                                [(0,1),(0,0),(0,-1),(-1,0)]]
        elif self.blocknum == J_MINO:
            self.rotationList = [[(1,1),(-1,0),(0,0),(1,0)],
                                [(1,-1),(0,1),(0,0),(0,-1)],
                                [(-1,-1),(1,0),(0,0),(-1,0)],
                                [(-1,1),(0,-1),(0,0),(0,1)]]
        elif self.blocknum == L_MINO:
            self.rotationList = [[(-1,1),(-1,0),(0,0),(1,0)],
                                [(1,1),(0,1),(0,0),(0,-1)],
                                [(1,-1),(1,0),(0,0),(-1,0)],
                                [(-1,-1),(0,-1),(0,0),(0,1)]]
        elif self.blocknum == S_MINO:
            self.rotationList = [[(-1,-1),(0,-1),(0,0),(1,0)],
                                [(-1,1),(-1,0),(0,0),(0,-1)],
                                [(1,1),(0,1),(0,0),(-1,0)],
                                [(1,-1),(1,0),(0,0),(0,1)]]
        elif self.blocknum == Z_MINO:
            self.rotationList = [[(1,-1),(0,-1),(0,0),(-1,0)],
                                [(-1,-1),(-1,0),(0,0),(0,1)],
                                [(-1,1),(0,1),(0,0),(1,0)],
                                [(1,1),(1,0),(0,0),(0,-1)]]
        else:
            print "Somehthing has gone terribly wrong."
            self.rotationList = None
        self.rotation = 0
        self.x = 4 #swap out literal
        self.y = 1
        self.blockGroup = pygame.sprite.Group()
        self.blockList = []
        for i in range(0,4):
            block = Block(self.blocknum)
            dx, dy = self.rotationList[self.rotation][i]
            self.blockList.append(block)
            self.blockGroup.add(block)

        self.updateBlocks(self.x, self.y)
        self.locked = False

        self.ghostBlockList = []
        for i in range(0, 4):
            ghostBlock = Block(GHOST)
            self.ghostBlockList.append(ghostBlock)
            self.blockGroup.add(ghostBlock)
        self.updateGhostBlocks()

    def updateBlocks(self, x = None, y = None):
        for i in range(0, 4):
            if x != None:
                self.x = x
            if y!= None:
                self.y = y
            (dx, dy) = self.rotationList[self.rotation][i]
            self.blockList[i].x = self.x+dx
            self.blockList[i].y = self.y+dy
            self.blockList[i].rect = (25*(self.x+dx)+100,25*(self.y+dy)+100)
        #starting numbers here should not be literal, use a var

    def updateGhostBlocks(self):
        for i in range(0, 4):
            (hx, hy) = self.hardDropLocation()
            (dx, dy) = self.rotationList[self.rotation][i]
            self.ghostBlockList[i].x = hx+dx
            self.ghostBlockList[i].y = hy+dy
            self.ghostBlockList[i].rect = (25*(hx+dx)+100,25*(hy+dy)+100)

    def canMove(self, direction):
        canMove = True
        for block in self.blockList:
            if direction == LEFT and (block.x <= 0 or self.board.blockMatrix[block.y][block.x-1]):
                canMove = False
            elif direction == RIGHT and (block.x >= 9 or self.board.blockMatrix[block.y][block.x+1]):
                canMove = False
            elif direction == DOWN and (block.y >= 19 or self.board.blockMatrix[block.y+1][block.x]):
                canMove = False
                self.locked = True
        return canMove

    #TODO: this needs a little work, if it can't rotate it should push out and then rotate instead of doing nothing
    def canRotate(self, direction):
        canRotate = True
        if direction == CLOCK:
            for (dx, dy) in self.rotationList[(self.rotation+1) % 4]:
                if self.x+dx < 0 or self.x+dx > 9 or self.y+dy > 19:
                    canRotate = False
        elif direction == COUNTERCLOCK:
            for (dx, dy) in self.rotationList[(self.rotation-1) % 4]:
                if self.x+dx < 0 or self.x+dx > 9 or self.y+dy > 19:
                    canRotate = False
        return canRotate

    def moveMino(self, direction):
        if direction == DOWN and self.canMove(DOWN):
            self.updateBlocks(x = None, y = self.y+1)
        elif direction == RIGHT and self.canMove(RIGHT):
            self.updateBlocks(x = self.x+1, y = None)
        elif direction == LEFT and self.canMove(LEFT):
            self.updateBlocks(x = self.x-1, y = None)

    def rotateMino(self, direction):
        if direction == CLOCK and self.canRotate(COUNTERCLOCK):
            self.rotation = (self.rotation+1) % 4
        elif direction == COUNTERCLOCK and self.canRotate(CLOCK):
            self.rotation = (self.rotation-1) % 4
        self.updateBlocks()

    def updateMino(self, hardDrop, dropOne, moveDir, rotateDir):
        if self.locked:
            self.placeMino()
            return True
        if hardDrop:
            x, y = self.hardDropLocation()
            self.updateBlocks(x = x, y = y)
            self.locked = True
        elif dropOne:
            self.moveMino(DOWN)
        if moveDir != None:
            self.moveMino(moveDir)
        if rotateDir != None:
            self.rotateMino(rotateDir)
        self.updateGhostBlocks()
        return False

    def hardDropLocation(self):
        minDiff = 20
        for block in self.blockList:
            diff = self.board.highestList[block.x]-1 - block.y
            if diff < minDiff:
                minDiff = diff
        return (self.x, self.y+minDiff)

    def placeMino(self):
        for block in self.blockList:
            self.board.blockMatrix[block.y][block.x] = block
            self.board.blockGroup.add(block)
            if block.y < self.board.highestList[block.x]:
                self.board.highestList[block.x] = block.y

class Block(pygame.sprite.Sprite):
    """A tetrimino block. """
    def __init__(self, blocknum):
        pygame.sprite.Sprite.__init__(self)
        blockstr = "block" + str(blocknum) + ".png"
        self.image, self.rect = load_image(blockstr)
        self.x = None
        self.y = None
