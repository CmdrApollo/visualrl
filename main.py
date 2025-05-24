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

    audio_handler = AudioHandler({
        "battle_theme": pygame.mixer.Sound(os.path.join("assets", "audio", "battle.wav")),
        "exploration_theme": pygame.mixer.Sound(os.path.join("assets", "audio", "exploration.wav")),

        "walk": pygame.mixer.Sound(os.path.join("assets", "audio", "walk.wav")),
    })

    audio_handler.play_song("exploration_theme", loops=-1)

    scene_manager = SceneManager()
    overworld_scene = OverworldScene("world.txt")
    scene_manager.add_scene("Overworld", overworld_scene)
    scene_manager.set_current_scene("Overworld")

    run = True
    while run:
        delta = clock.tick_busy_loop(60) / 1000.0

        if delta:
            pygame.display.set_caption(f"{GAMENAME} - FPS: {int(1 / delta)}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                scene_manager.current_scene.on_input(event.key, audio_handler)
        
        scene_manager.current_scene.update(delta, audio_handler)

        screen.fill('black')

        scene_manager.current_scene.draw(screen)

        WIN.blit(pygame.transform.scale(screen, (WIDTH * 2, HEIGHT * 2)), (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()