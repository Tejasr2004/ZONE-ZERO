import pygame
import sys
import os
from settings import *
from player import Player
from map import Map, Wall, Tree, Floor
from camera import Camera
from mobs import Zombie
from inventory import Item, Inventory

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.game_folder = os.path.dirname(__file__)
        assets_folder = os.path.join(self.game_folder, 'assets')
        self.wall_img = pygame.image.load(os.path.join(assets_folder, 'wall.png')).convert()
        self.grass_img = pygame.image.load(os.path.join(assets_folder, 'grass.png')).convert()
        self.tree_img = pygame.image.load(os.path.join(assets_folder, 'tree.png')).convert_alpha()
        self.floor_img = pygame.image.load(os.path.join(assets_folder, 'floor.png')).convert()
        self.player_img = pygame.image.load(os.path.join(assets_folder, 'player.png')).convert_alpha()
        self.zombie_img = pygame.image.load(os.path.join(assets_folder, 'zombie.png')).convert_alpha()
        self.apple_img = pygame.image.load(os.path.join(assets_folder, 'apple.png')).convert_alpha()
        self.water_img = pygame.image.load(os.path.join(assets_folder, 'water.png')).convert_alpha()
        self.medkit_img = pygame.image.load(os.path.join(assets_folder, 'medkit.png')).convert_alpha()
        self.font = pygame.font.SysFont("arial", 20)

    def new(self):
        # Initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.map = Map(self)
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == 'T':
                    Tree(self, col, row)
                if tile == 'F':
                    Floor(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'Z':
                    Zombie(self, col, row)
                if tile == 'A':
                    Item(self, (col*TILESIZE, row*TILESIZE), 'apple')
                if tile == 'O': # O for Water (W is wall)
                    Item(self, (col*TILESIZE, row*TILESIZE), 'water')
                if tile == 'M':
                    Item(self, (col*TILESIZE, row*TILESIZE), 'medkit')
                    
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # Game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)
        
        # Mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.player.health -= 1
            if self.player.health <= 0:
                self.playing = False # Game Over

    def draw_hud(self):
        # Draw Health Bar
        draw_bar(self.screen, 10, 10, self.player.health, 100, RED)
        # Draw Hunger Bar
        draw_bar(self.screen, 10, 40, self.player.hunger, 100, (200, 100, 0)) # Orange
        # Draw Thirst Bar
        draw_bar(self.screen, 10, 70, self.player.thirst, 100, (0, 0, 255)) # Blue

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BG_COLOR)
        
        # Draw grid relative to camera
        # We find the offset of the camera (modulo TILESIZE) to make it look infinite
        # For now, let's tile the grass background
        
        # Calculate visible range
        start_x = -self.camera.camera.x // TILESIZE
        start_y = -self.camera.camera.y // TILESIZE
        end_x = start_x + (WIDTH // TILESIZE) + 2
        end_y = start_y + (HEIGHT // TILESIZE) + 2
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                # Calculate screen position
                screen_x = x * TILESIZE + self.camera.camera.x
                screen_y = y * TILESIZE + self.camera.camera.y
                self.screen.blit(self.grass_img, (screen_x, screen_y))

        # Draw sprites with camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
        # Draw HUD
        self.draw_hud()
        
        # Draw Inventory
        self.player.inventory.draw(self.screen)
        
        # Draw Credits
        text_surf = self.font.render("Created by Tejas R Gowda", True, WHITE)
        self.screen.blit(text_surf, (WIDTH - text_surf.get_width() - 10, HEIGHT - 30))
            
        pygame.display.flip()

    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_e:
                    # Pick up item
                    hits = pygame.sprite.spritecollide(self.player, self.items, True)
                    for hit in hits:
                        self.player.inventory.add_item(hit.type)
                if event.key == pygame.K_1:
                    # Use Item? For now simpler logic: Consume items automatically?
                    # Or 'i' to use items. Let's just consume on pickup for stats + inventory demo
                    pass

def draw_bar(surf, x, y, pct, max_val, color):
    if pct < 0: pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = (pct / max_val) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


if __name__ == '__main__':
    g = Game()
    while True:
        g.new()
        g.run()
