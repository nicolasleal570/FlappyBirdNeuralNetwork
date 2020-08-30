import pygame
import os

# Floor image
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))


class Base:
    VEL = 5  # Velocity
    width = BASE_IMG.get_width()  # Image width
    IMG = BASE_IMG

    def __init__(self, y):
        """ Constructor. """
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        """Move and animation of the floor."""
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        """Drawing floor images. """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
