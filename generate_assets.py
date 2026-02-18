import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
TILESIZE = 64
ASSETS_DIR = 'assets'

def create_grass():
    surf = pygame.Surface((TILESIZE, TILESIZE))
    surf.fill((34, 139, 34))  # Forest Green
    # Add some noise
    for _ in range(20):
        x = int(pygame.math.Vector2(0, TILESIZE).x + pygame.time.get_ticks() % TILESIZE) # Randomish
        # Actually proper random is better
        import random
        x = random.randint(0, TILESIZE-1)
        y = random.randint(0, TILESIZE-1)
        color = (0, 100, 0)
        pygame.draw.circle(surf, color, (x, y), 2)
    return surf

def create_wall():
    surf = pygame.Surface((TILESIZE, TILESIZE))
    surf.fill((139, 69, 19))  # SaddleBrown (Brick base)
    # Draw brick lines
    color = (100, 50, 10)
    for y in range(0, TILESIZE, 16):
        pygame.draw.line(surf, color, (0, y), (TILESIZE, y), 2)
        offset = 0 if (y // 16) % 2 == 0 else 16
        for x in range(offset, TILESIZE, 32):
            pygame.draw.line(surf, color, (x, y), (x, y + 16), 2)
    return surf

def create_tree():
    surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
    # Trunk
    pygame.draw.rect(surf, (101, 67, 33), (24, 40, 16, 24))
    # Leaves
    pygame.draw.circle(surf, (0, 100, 0), (32, 24), 24)
    pygame.draw.circle(surf, (0, 120, 0), (32, 24), 18)
    return surf

def create_floor():
    surf = pygame.Surface((TILESIZE, TILESIZE))
    surf.fill((210, 180, 140))  # Tan
    # Wood planks
    color = (139, 69, 19)
    for x in range(0, TILESIZE, 16):
        pygame.draw.line(surf, color, (x, 0), (x, TILESIZE), 2)
    return surf

    print("Assets generated in /assets")

def create_zombie():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surf, (0, 150, 0), (16, 16), 16) # Green Head
    pygame.draw.circle(surf, (255, 0, 0), (10, 12), 3) # Red Eye
    pygame.draw.circle(surf, (255, 0, 0), (22, 12), 3) # Red Eye
    return surf

def create_apple():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 0, 0), (16, 16), 12) # Red Apple
    pygame.draw.line(surf, (139, 69, 19), (16, 4), (16, 10), 2) # Stem
    return surf

def create_water():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 0, 255), (8, 8, 16, 24)) # Blue Bottle
    return surf

def create_medkit():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255, 255, 255), (4, 8, 24, 16)) # White Box
    pygame.draw.line(surf, (255, 0, 0), (16, 10), (16, 22), 4) # Red Cross V
    pygame.draw.line(surf, (255, 0, 0), (10, 16), (22, 16), 4) # Red Cross H
    return surf

def main():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    grass = create_grass()
    pygame.image.save(grass, os.path.join(ASSETS_DIR, 'grass.png'))
    wall = create_wall()
    pygame.image.save(wall, os.path.join(ASSETS_DIR, 'wall.png'))
    tree = create_tree()
    pygame.image.save(tree, os.path.join(ASSETS_DIR, 'tree.png'))
    floor = create_floor()
    pygame.image.save(floor, os.path.join(ASSETS_DIR, 'floor.png'))
    player = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(player, (255, 255, 0), (16, 16), 16)
    pygame.draw.circle(player, (0, 0, 0), (10, 12), 3)
    pygame.draw.circle(player, (0, 0, 0), (22, 12), 3)
    pygame.image.save(player, os.path.join(ASSETS_DIR, 'player.png'))

    # New Assets
    zombie = create_zombie()
    pygame.image.save(zombie, os.path.join(ASSETS_DIR, 'zombie.png'))
    apple = create_apple()
    pygame.image.save(apple, os.path.join(ASSETS_DIR, 'apple.png'))
    water = create_water()
    pygame.image.save(water, os.path.join(ASSETS_DIR, 'water.png'))
    medkit = create_medkit()
    pygame.image.save(medkit, os.path.join(ASSETS_DIR, 'medkit.png'))

    print("Assets generated in /assets")

if __name__ == '__main__':
    main()
