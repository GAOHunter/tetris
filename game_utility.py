import os, sys
import pygame
from pygame.locals import *

#global constants
I_MINO = 1
O_MINO = 2
T_MINO = 3
J_MINO = 4
L_MINO = 5
S_MINO = 6
Z_MINO = 7

DOWN = 10
RIGHT = 11
LEFT = 12

CLOCK = 20
COUNTERCLOCK = 21

def load_image(name, colorkey=None):
    fullname = os.path.join('tetrisdata', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoSound:
        def play(self) : pass
    if not pygame.mixer:
        return NoSound()
    fullname = os.path.join('tetrisdata', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound
