import pygame
import math
from settings import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 100
        self.vx = 0
        self.vy = 0

    def update(self):
        # Simple AI: Move towards player
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < 400: # Chase range
            angle = math.atan2(dy, dx)
            self.vx = math.cos(angle) * self.speed
            self.vy = math.sin(angle) * self.speed
        else:
            self.vx = 0
            self.vy = 0
            
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
