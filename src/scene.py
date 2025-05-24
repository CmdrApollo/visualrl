import random
import pygame
import math

from constants import WORLD_WIDTH, WORLD_HEIGHT, lerp

from .entity import Entity
from .draw import *

arrow_tile = 0xff

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_current_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found.")

class GameScene:
    def __init__(self, name):
        self.name = name
        self.entities = []
    
    def on_input(self, key, audio=None):
        pass
    
    def update(self, delta, audio=None):
        pass
        
    def draw(self, screen):
        pass

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

class MainMenuScene(GameScene):
    def __init__(self):
        super().__init__("Main Menu")
        self.title_image = pygame.image.load(os.path.join("assets", "gfx", "title.png"))
        self.title_image.set_colorkey((0, 0, 0))

        self.selected_option = 0

    def on_input(self, key, audio=None):
        if key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % 3
        elif key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % 3
        elif key == pygame.K_RETURN:
            if self.selected_option == 0:
                return "Overworld"
            if self.selected_option == 1:
                return "Overworld"
            elif self.selected_option == 2:
                return "Exit"

    def draw(self, screen):
        t = pygame.time.get_ticks() / 70
        t %= TILESIZE

        for x in range(WORLD_WIDTH + 1):
            for y in range(WORLD_HEIGHT + 1):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, '#202020', (x * TILESIZE - t, y * TILESIZE - t, TILESIZE, TILESIZE))

        screen.blit(self.title_image, (WIDTH // 2 - self.title_image.get_width() // 2, 5 + 5 * math.sin(pygame.time.get_ticks() / 500)))
        ax = WORLD_WIDTH // 2 - 3
        ay = 8.5 + self.selected_option
        draw_tile(screen, ax + math.sin(pygame.time.get_ticks() / 250) * 0.1, ay, arrow_tile, True, 0)

        draw_text(screen, "New Game", WORLD_WIDTH // 2, 8.5, 'white', center=True)
        draw_text(screen, "Old Game", WORLD_WIDTH // 2, 9.5, 'white', center=True)
        draw_text(screen, "Don't Play", WORLD_WIDTH // 2, 10.5, 'white', center=True)

class OverworldScene(GameScene):
    def __init__(self, filename):
        super().__init__("Overworld")
        self.player = Entity(1, 1, 0x80)
        self.entities = [Entity(3, 7, 0x81)]
        self.world, self.passable = load_from_file(filename)
        self.tx, self.ty = 1, 1

    def generate_world(self):
        self.world.clear()
        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                t = 1
                if x == 0 or x == WORLD_WIDTH - 1 or y == 0 or y == WORLD_HEIGHT - 1:
                    t = 0
                self.world.append(t)
    
    def on_input(self, key, audio=None):
        ax, ay = 0, 0

        if key == pygame.K_UP:
            ay = -1
            ax = 0
        elif key == pygame.K_DOWN:
            ay = 1
            ax = 0
        elif key == pygame.K_LEFT:
            ax = -1
            ay = 0
        elif key == pygame.K_RIGHT:
            ax = 1
            ay = 0

        self.tx += ax
        self.ty += ay

        if not self.passable[self.ty * WORLD_WIDTH + self.tx]:
            self.tx -= ax
            self.ty -= ay
        else:
            if audio and (ax or ay):
                audio.play_sound("walk")

    def update(self, delta, audio=None):
        self.player.x = lerp(self.player.x, self.tx, 0.2)
        self.player.y = lerp(self.player.y, self.ty, 0.2)

        if abs(self.player.x - self.tx) < 0.05 and abs(self.player.y - self.ty) < 0.05:
            self.player.x = self.tx
            self.player.y = self.ty
            self.player.rotation = 0
        else:
            self.player.rotation = math.sin(pygame.time.get_ticks() / 100) * 10
    
    def draw(self, screen):
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                t = self.world[y * WORLD_WIDTH + x]
                draw_tile(screen, x, y, t)

        for entity in self.entities:
            entity.draw(screen)

        self.player.draw(screen)