import pygame
import os

from constants import *

TILESHEET = pygame.image.load(os.path.join("assets", "gfx", "tilesheet.png")).convert_alpha()

TILESHEET.set_colorkey((0, 0, 0))

global_font = 'comicsansms'

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

def draw_tile(screen, x, y, index, alpha=False, rotation=0, scale=1):
    i, j = index % 16, index // 16
    if not alpha:
        pygame.draw.rect(screen, 'black', (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE))
    s = TILESHEET.subsurface(i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE).copy()
    
    if rotation != 0:
        s = pygame.transform.rotate(s, rotation)

    if scale != 1:
        s = pygame.transform.scale(s, (int(TILESIZE * scale), int(TILESIZE * scale)))

    screen.blit(s, (x * TILESIZE + TILESIZE / 2 - s.get_width() / 2, y * TILESIZE + TILESIZE / 2 - s.get_height() / 2))

def draw_text(screen, text, x, y, color='white', font_size=24, center=False):
    font = pygame.font.SysFont(global_font, font_size)
    text_surface = font.render(text, True, color)
    if center:
        screen.blit(text_surface, (x * TILESIZE + TILESIZE / 2 - text_surface.get_width() / 2, y * TILESIZE + TILESIZE / 2 - text_surface.get_height() / 2))
    else:
        screen.blit(text_surface, (x * TILESIZE, y * TILESIZE))

def measure_text(text, font_size=24):
    font = pygame.font.SysFont(global_font, font_size)
    return font.size(text)