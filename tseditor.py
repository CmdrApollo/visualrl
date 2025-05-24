import pygame
import math
import random

GAMENAME = "eRPG"

from constants import *

from src.entity import Entity
from src.draw import *

from src.scene import SceneManager, GameScene, OverworldScene
from src.AudioHandler import AudioHandler

def main():
    clock = pygame.time.Clock()

    color = 'white'
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
                    pass
                        
        if pygame.mouse.get_pressed()[0]:
            mx, my = event.pos
            x = mx // 2 // TILESIZE
            y = my // 2 // TILESIZE
            sx = mx // 2 // 8
            sy = my // 2 // 8

            if tab:
                selected_tile = (y * 16 + x) % 128
            else:
                if sx < 32 and sy < 32:
                    TILESHEET.subsurface(selected_tile % 16 * TILESIZE, selected_tile // 16 * TILESIZE, TILESIZE, TILESIZE).set_at((sx, sy), color)

        screen.fill('darkgrey')

        if tab:
            for i in range(128):
                x = i % 16
                y = i // 16
                tile_id = i
                if tile_id is not None:
                    draw_tile(screen, x, y, tile_id)
                if i == selected_tile:
                    pygame.draw.rect(screen, 'white', (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE), 4)
        else:
            screen.blit(pygame.transform.scale(TILESHEET.subsurface(selected_tile % 16 * TILESIZE, selected_tile // 16 * TILESIZE, TILESIZE, TILESIZE), (32 * 8, 32 * 8)), (0, 0))

        WIN.blit(pygame.transform.scale(screen, (WIDTH * 2, HEIGHT * 2)), (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()