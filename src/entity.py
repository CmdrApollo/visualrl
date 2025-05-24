from .draw import *

class Entity:
    def __init__(self, x, y, t_id, nframes=1, alpha=True):
        self.x = x
        self.y = y
        self.t_id = t_id
        self.alpha = alpha
        self.rotation = 0

    def draw(self, screen):
        draw_tile(screen, self.x, self.y, self.t_id, self.alpha, self.rotation)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        self.x = x
        self.y = y