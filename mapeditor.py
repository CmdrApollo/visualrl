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
    zipped = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                zipped.extend(int(x) for x in line.split())
    except FileNotFoundError:
        print(f"File {filename} not found. Generating default world.")
        world, passable = [1] * (WORLD_WIDTH * WORLD_HEIGHT), [True] * (WORLD_WIDTH * WORLD_HEIGHT)
        return world, passable

    world = zipped[::2]
    passable = zipped[1::2]

    return world, passable

def main():
    clock = pygame.time.Clock()
    
    world, passable = load_from_file('world.txt')

    selected_tile = 0

    run = True
    while run:
        delta = clock.tick_busy_loop(60) / 1000.0

        tab = pygame.key.get_pressed()[pygame.K_TAB]
        ctrl = pygame.key.get_pressed()[pygame.K_LCTRL]

        if delta:
            pygame.display.set_caption(f"{GAMENAME} - FPS: {int(1 / delta)}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and ctrl:
                    mx, my = event.pos
                    x = mx // 2 // TILESIZE
                    y = my // 2 // TILESIZE
                    if 0 <= x < WORLD_WIDTH and 0 <= y < WORLD_HEIGHT:
                        passable[y * WORLD_WIDTH + x] = not passable[y * WORLD_WIDTH + x]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open('world.txt', 'w') as f:
                        for i in range(WORLD_HEIGHT):
                            for j in range(WORLD_WIDTH):
                                f.write(f"{world[i * WORLD_WIDTH + j]} {int(passable[i * WORLD_WIDTH + j])} ")
                            f.write("\n")
                        
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            x = mx // 2 // TILESIZE
            y = my // 2 // TILESIZE

            if tab:
                selected_tile = (y * 16 + x) % 128
            elif not ctrl:
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
                        if ctrl and not passable[y * WORLD_WIDTH + x]:
                            pygame.draw.rect(screen, 'red', (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE), 2)

        WIN.blit(pygame.transform.scale(screen, (WIDTH * 2, HEIGHT * 2)), (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()