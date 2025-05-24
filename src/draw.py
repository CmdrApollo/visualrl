import pygame
import os

from constants import *

TILESHEET = pygame.image.load(os.path.join("assets", "gfx", "tilesheet.png")).convert_alpha()

TILESHEET.set_colorkey((0, 0, 0))

class Colors:
    RED = '#FF8080'
    GREEN = '#80FF80'
    BLUE = '#8080FF'
    YELLOW = '#FFFF80'
    CYAN = '#80FFFF'
    MAGENTA = '#FF80FF'
    WHITE = '#FFFFFF'
    BLACK = '#000000'
    ORANGE = '#FFA500'
    PURPLE = '#800080'
    PINK = '#FFC0CB'
    BROWN = '#A52A2A'
    GRAY = '#808080'

def draw_tile(screen, x, y, index, alpha=False, rotation=0):
    i, j = index % 16, index // 16
    if not alpha:
        pygame.draw.rect(screen, 'black', (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE))
    s = TILESHEET.subsurface(i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE).copy()
    
    if rotation != 0:
        s = pygame.transform.rotate(s, rotation)

    screen.blit(s, (x * TILESIZE + TILESIZE / 2 - s.get_width() / 2, y * TILESIZE + TILESIZE / 2 - s.get_height() / 2))