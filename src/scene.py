import random
import pygame
import math

from constants import WORLD_WIDTH, WORLD_HEIGHT, lerp

from .entity import Entity
from .draw import *

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
    world = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                world.extend(int(x) for x in line.split())
    except FileNotFoundError:
        print(f"File {filename} not found. Generating default world.")
        world = [1] * (WORLD_WIDTH * WORLD_HEIGHT)
    return world

class OverworldScene(GameScene):
    def __init__(self, filename):
        super().__init__("Overworld")
        self.player = Entity(5, 5, 0x80)
        self.entities = [Entity(3, 7, 0x81)]
        self.world = load_from_file(filename)
        self.tx, self.ty = 5, 5

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

        if self.world[self.ty * WORLD_WIDTH + self.tx] == 0:
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
                draw_tile(screen, x, y, self.world[y * WORLD_WIDTH + x])

        for entity in self.entities:
            entity.draw(screen)

        self.player.draw(screen)