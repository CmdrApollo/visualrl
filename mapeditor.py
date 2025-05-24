import pygame
import math
import random

GAMENAME = "eRPG"

from constants import *

from src.entity import Entity
from src.draw import *

from src.scene import SceneManager, GameScene, OverworldScene
from src.AudioHandler import AudioHandler

def load_from_file(filename):
    world = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                world.extend(int(x) for x in line.split())
    except FileNotFoundError:
        print(f"File {filename} not found. Generating default world.")
        world = [1] * (WORLD_WIDTH * WORLD_HEIGHT)
    return world

def main():
    clock = pygame.time.Clock()
    
    world = load_from_file('world.txt')

    selected_tile = 0

    run = True
    while run:
        delta = clock.tick_busy_loop(60) / 1000.0

        tab = pygame.key.get_pressed()[pygame.K_TAB]

        if delta:
            pygame.display.set_caption(f"{GAMENAME} - FPS: {int(1 / delta)}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open('world.txt', 'w') as f:
                        for i in range(WORLD_HEIGHT):
                            for j in range(WORLD_WIDTH):
                                f.write(f"{world[i * WORLD_WIDTH + j]} ")
                            f.write("\n")
                        
        if pygame.mouse.get_pressed()[0]:
            mx, my = event.pos
            x = mx // TILESIZE
            y = my // TILESIZE

            if tab:
                selected_tile = (y * 16 + x) % 128
            else:
                if 0 <= x < WORLD_WIDTH and 0 <= y < WORLD_HEIGHT:
                    world[y * WORLD_WIDTH + x] = selected_tile

        screen.fill('black')

        if tab:
            screen.fill('blue')

            for i in range(128):
                x = i % 16
                y = i // 16
                tile_id = i
                if tile_id is not None:
                    draw_tile(screen, x, y, tile_id)
                if i == selected_tile:
                    pygame.draw.rect(screen, 'white', (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE), 4)
        else:
            for x in range(WORLD_WIDTH):
                for y in range(WORLD_HEIGHT):
                    tile_id = world[y * WORLD_WIDTH + x]
                    if tile_id is not None:
                        draw_tile(screen, x, y, tile_id)

        WIN.blit(screen, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()