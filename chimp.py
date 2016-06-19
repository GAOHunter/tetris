#intro from http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
import os, sys
import pygame
from pygame.locals import *

#if not pygame.mixer: print 'Warning, sound disabled'
if not pygame.font: print 'Warn_ing, fonts disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('chimpdata', name)
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
    fullname = os.path.join('chimpdata', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound

class Fist(pygame.sprite.Sprite):
    """Moves a clenched fist, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('fist.jpg', -1)
        self.punching = 0

    def update(self):
        """Move the fist based on the mouse position"""
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5,10)

    def punch(self, target):
        """Returns true if fist collides with the target"""
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """Called to pull the fist back"""
        self.punching = 0

class Chimp(pygame.sprite.Sprite):
    """Moves a monkey critter across the screen. It can spin the monkeywhen it is punched"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('chimp.gif', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        """Walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self.spin()
        else:
            self.walk()

    def walk(self):
        """Move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def spin(self):
        """Spin the monkey image"""
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center = center)

    def punched(self):
        """This will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

def main():
    """This function is called when the program starts.
        It initializes everything it needs, then runs 
        in a loop until the function returns."""
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 60))
    pygame.display.set_caption("Monkey Fever")
    pygame.mouse.set_visible(0)

    #Create Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #Put Text on Background, Center
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10 , 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    #Display the Background
    screen.blit(background, (0,0))
    pygame.display.flip()

    #Prepare Game Objects
    clock = pygame.time.Clock()
    #whiff_sound = load_sound("whiff.wav")
    #punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))

    #Main Loop
    while 1:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    #punch_sound.play()
                    chimp.punched()
                #else:
                    #whiff_sound.play()
            elif event.type is MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        #Draw Everything
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()

    #Game Over

if __name__ == '__main__': main()