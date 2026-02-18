import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        if type == 'apple':
            self.image = game.apple_img
        elif type == 'water':
            self.image = game.water_img
        elif type == 'medkit':
            self.image = game.medkit_img
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Inventory:
    def __init__(self, game):
        self.game = game
        self.items = []
        self.capacity = 5

    def add_item(self, item_type):
        if len(self.items) < self.capacity:
            self.items.append(item_type)
            print(f"Added {item_type}. Inventory: {self.items}")
            return True
        else:
            print("Inventory Full!")
            return False

    def draw(self, screen):
        # Draw inventory at bottom center
        start_x = WIDTH // 2 - (self.capacity * 40) // 2
        y = HEIGHT - 50
        for i in range(self.capacity):
            x = start_x + i * 40
            rect = pygame.Rect(x, y, 32, 32)
            pygame.draw.rect(screen, LIGHTGREY, rect, 2)
            
            if i < len(self.items):
                item_type = self.items[i]
                img = None
                if item_type == 'apple': img = self.game.apple_img
                elif item_type == 'water': img = self.game.water_img
                elif item_type == 'medkit': img = self.game.medkit_img
                
                if img:
                    screen.blit(pygame.transform.scale(img, (24, 24)), (x+4, y+4))
