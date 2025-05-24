import pygame

pygame.init()

WORLD_WIDTH, WORLD_HEIGHT = 16, 12

TILESIZE = 32

WIDTH, HEIGHT = WORLD_WIDTH * TILESIZE, WORLD_HEIGHT * TILESIZE
WIN = pygame.display.set_mode((WIDTH * 2, HEIGHT * 2))
screen = pygame.Surface((WIDTH, HEIGHT))

def lerp(a, b, t):
    return a + (b - a) * t

def sign(x):
    return (x > 0) - (x < 0)