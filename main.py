import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1280, 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT))

WORLD_WIDTH, WORLD_HEIGHT = 30, 20

TILESHEET = pygame.image.load("monochrome_packed.png").convert_alpha()

TILESHEET = pygame.transform.scale(TILESHEET, (TILESHEET.get_width() * 2, TILESHEET.get_height() * 2))

TILESHEET.set_colorkey((0, 0, 0))

TILESIZE = 32

def lerp(a, b, t):
    return a + (b - a) * t

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

def draw_tile(screen, x, y, index, color='white', alpha=False, rotation=0):
    i, j = index % 49, index // 49
    if not alpha:
        pygame.draw.rect(screen, 'black', (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE))
    s = TILESHEET.subsurface(i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE).copy()
    
    if color != 'white':
        s.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    
    if rotation != 0:
        s = pygame.transform.rotate(s, rotation)

    screen.blit(s, (x * TILESIZE + TILESIZE / 2 - s.get_width() / 2, y * TILESIZE + TILESIZE / 2 - s.get_height() / 2))

def draw_frame(screen, x, y, w, h, color='white', alpha=False, filled=True):
    for i in range(w):
        for j in range(h):
            if i == 0 and j == 0:
                draw_tile(screen, x + i, y + j, 15 + 49 * 4, color=color, alpha=alpha, rotation=0)
            elif i == 0 and j == h - 1:
                draw_tile(screen, x + i, y + j, 15 + 49 * 4, color=color, alpha=alpha, rotation=90)
            elif i == w - 1 and j == h - 1:
                draw_tile(screen, x + i, y + j, 15 + 49 * 4, color=color, alpha=alpha, rotation=180)
            elif i == w - 1 and j == 0:
                draw_tile(screen, x + i, y + j, 15 + 49 * 4, color=color, alpha=alpha, rotation=270)
            else:
                if i == 0 or i == w - 1 or j == 0 or j == h - 1:
                    draw_tile(screen, x + i, y + j, 14 + 49 * 4, color=color, alpha=alpha, rotation=90 * (1 - (i == 0 or i == w - 1)))
                elif filled:
                    draw_tile(screen, x + i, y + j, 0, color=color, alpha=alpha, rotation=0)

class Entity:
    def __init__(self, x, y, t_id, color='white', alpha=False):
        self.x = x
        self.y = y
        self.t_id = t_id
        self.color = color
        self.alpha = alpha
        self.rotation = 0

    def draw(self):
        draw_tile(screen, self.x, self.y, self.t_id, self.color, self.alpha, self.rotation)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        self.x = x
        self.y = y

def draw_text(screen, text, x, y, color='white', alpha=True):
    i = 0
    j = 0

    spec_chars = "0123456789:.%"

    for char in text.upper():
        if char == '\n':
            j += 1
            i = 0
        else:
            if char.isalpha():
                a = ord(char) - 65
                draw_tile(screen, x + i, y + j, a % 13 + (18 + a // 13) * 49 + 35, color=color, alpha=alpha)
            elif char in spec_chars:
                a = spec_chars.index(char)
                draw_tile(screen, x + i, y + j, a + 17 * 49 + 35, color=color, alpha=alpha)
            elif char == '!':
                draw_tile(screen, x + i, y + j, 35 + 13 * 49, color=color, alpha=alpha)
            elif char == '?':
                draw_tile(screen, x + i, y + j, 37 + 13 * 49, color=color, alpha=alpha)
            i += 1

def main():
    clock = pygame.time.Clock()

    world = []
    
    for y in range(WORLD_HEIGHT):
        for x in range(WORLD_WIDTH):
            t = random.choice([5, 6, 7])
            if x == 0 or x == WORLD_WIDTH - 1 or y == 0 or y == WORLD_HEIGHT - 1:
                t = 16
            world.append(t)

    player = Entity(5, 5, 30, Colors.BLUE)
    entities = [Entity(3, 7, 30 + 49 * 3, Colors.ORANGE)]

    tx, ty = 5, 5

    run = True
    while run:
        delta = clock.tick_busy_loop(60) / 1000.0

        if delta:
            pygame.display.set_caption(f"FPS: {int(1 / delta)}")

        ax, ay = 0, 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ay -= 1
                elif event.key == pygame.K_DOWN:
                    ay += 1
                elif event.key == pygame.K_LEFT:
                    ax -= 1
                elif event.key == pygame.K_RIGHT:
                    ax += 1
        
        if ax != 0 or ay != 0:            
            tx += ax
            ty += ay

            if world[ty * WORLD_WIDTH + tx] == 16:
                tx -= ax
                ty -= ay

        player.x = lerp(player.x, tx, 0.2)
        player.y = lerp(player.y, ty, 0.2)

        if abs(player.x - tx) < 0.05 and abs(player.y - ty) < 0.05:
            player.x = tx
            player.y = ty
            player.rotation = 0
        else:
            player.rotation = math.sin(pygame.time.get_ticks() / 100) * 10
        
        screen.fill((0, 0, 0))

        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                if world[y * WORLD_WIDTH + x] == 16:
                    draw_tile(screen, x, y, world[y * WORLD_WIDTH + x], Colors.GRAY)
                else:
                    draw_tile(screen, x, y, world[y * WORLD_WIDTH + x], Colors.GREEN)

        for entity in entities:
            entity.draw()

        player.draw()

        draw_text(screen, "Townville", 1, 0, Colors.YELLOW, alpha=True)
        
        draw_frame(screen, 14, 0, 26, 10)
        draw_text(screen, "Hey this is pretty cool!", 15, 1)

        WIN.blit(screen, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()