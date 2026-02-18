import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Limit scrolling to map size (optional, for now infinite/unbounded)
        # x = min(0, max(x, -(self.width - WIDTH)))
        # y = min(0, max(y, -(self.height - HEIGHT)))
        
        self.camera = pygame.Rect(x, y, self.width, self.height)
