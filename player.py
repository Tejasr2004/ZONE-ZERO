import pygame
from settings import *
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = 0
        self.vy = 0
        
        # Stats
        self.health = PLAYER_HEALTH
        self.hunger = PLAYER_HUNGER
        self.thirst = PLAYER_THIRST
        self.last_update = 0
        
        # Inventory
        self.inventory = Inventory(game)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            
        # Normalize diagonal movement
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
            
        # Pickup (Handling in events is better for single press, but we can do a check here or main)
        # We'll handle single press in main events, but continuously checking proximity here is fine for now
        pass

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
        # Stats Decay
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000: # Every second
            self.last_update = now
            self.hunger -= HUNGER_DECAY
            self.thirst -= THIRST_DECAY
            if self.hunger <= 0 or self.thirst <= 0:
                self.health -= 1 # Starving/Dehydrated
            
            # Clamp
            self.health = max(0, min(self.health, 100))
            self.hunger = max(0, min(self.hunger, 100))
            self.thirst = max(0, min(self.thirst, 100))
            
    def heal(self, amount):
        self.health += amount
        if self.health > 100: self.health = 100
        
    def eat(self, amount):
        self.hunger += amount
        if self.hunger > 100: self.hunger = 100
        
    def drink(self, amount):
        self.thirst += amount
        if self.thirst > 100: self.thirst = 100

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
