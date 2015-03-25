import pygame
from pygame.locals import *
from pygame.color import *

display_flags = 0
display_size = (800,600)
from visual import Visualisation

class Progress(object):
    def __init__(self, every=1):
        self.every = every
        self.count = 0

        pygame.init()
        self.screen = pygame.display.set_mode(display_size, display_flags)
        self.width, self.height = self.screen.get_size()

        clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 16)

        self.viz = Visualisation()
        self.viz.set_size(self.width, self.height)

        # What we want to show in the debug format
        # self.viz.shapes = True
        # self.viz.joints = True
        # self.viz.aabb = True

        ### Physics stuff
        # space.damping = 0.999 # to prevent it from blowing up.
        # static_body = pm.Body()
        # mouse_body = pm.Body()
        self.running = True
        self.paused = False

    def begin(self, sim):
        self.count = 0

    def update(self, sim):
        if self.count % self.every == 0:
            self.draw(sim)
        self.count += 1

    def interact(self, sim):
        self.draw(sim)

    def end(self, sim):
        pass

    def draw(self, sim):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE:
                    self.paused = not self.paused
            elif event.type == MOUSEBUTTONDOWN:
                self.running = False

        ### Clear screen
        self.screen.fill(THECOLORS["black"])
        self.viz.render(self.screen, sim)

        ### Flip screen
        # self.screen.blit(font.render("Press left mouse button and drag to interact",
                                     # 1, THECOLORS["darkgrey"]),
                                     # (5,self.height - 35))
        self.screen.blit(
            self.font.render("frame: %d" % self.count, 1, THECOLORS["darkgrey"]),
                         (5,self.height - 20))
        if self.paused:
            self.screen.blit(
            self.font.render("PAUSED (press space)" , 1, THECOLORS["darkgrey"]),
                         (5,self.height - 40))
        #
        pygame.display.flip()
