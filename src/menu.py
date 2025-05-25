from constants import *
from src.draw import draw_text, measure_text

def draw_patchrect(screen, rect):
    pygame.draw.rect(screen, '#000000', rect, 0, border_radius=8)
    pygame.draw.rect(screen, '#ffffff', rect, 1, border_radius=8)    

class MenuObject:
    def __init__(self, name=None):
        self.name = 'root' if not name else name

        self.table = pygame.Vector2(1, 4)
        self.cell_size = pygame.Vector2()

        self.items = []
        self.cursor_pos = pygame.Vector2(0, 0)
        self.enabled = True
        self.rect = None

    def __getitem__(self, key):
        for item in self.items:
            if item.name == key:
                return item
        
        return None

    def CursorItem(self):
        i = int(self.cursor_pos.y * self.table.x + self.cursor_pos.x)

        return self.items[i]

    def Navigate(self, dx, dy):
        self.cursor_pos.x += dx
        self.cursor_pos.y += dy

        self.cursor_pos.x = max(0, min(self.cursor_pos.x, self.table.x - 1))
        self.cursor_pos.y = max(0, min(self.cursor_pos.y, self.table.y - 1))

        if (self.cursor_pos.y * self.table.x + self.cursor_pos.x) >= len(self.items):
            i = len(self.items) - 1

            self.cursor_pos.x = i % self.table.x
            self.cursor_pos.y = i // self.table.y

    def SetTable(self, x, y):
        self.table.x = x
        self.table.y = y

        return self

    def has_children(self):
        return bool(len(self.items))

    def build(self):
        if not len(self.items):
            return
        
        for child in self.items:
            child.build()
            
        x, y = max([measure_text(item.name, 26)[0] for item in self.items]), max([measure_text(item.name, 16)[1] for item in self.items])

        self.cell_size = pygame.Vector2(x, y)

        x *= self.table.x
        y *= self.table.y

        self.rect = pygame.Rect(0, 0, x + 16, y + 16)
    
    def draw(self, screen, offset):
        rect = self.rect.copy()

        rect.x += offset.x
        rect.y += offset.y

        draw_patchrect(screen, rect)

        x = offset.x + 10
        y = offset.y + 8

        xi = 0
        yi = 0

        for i in range(len(self.items)):
            draw_text(screen, self.items[i].name, x / TILESIZE, y / TILESIZE, '#ffffff', 16)

            if self.cursor_pos.x == xi and self.cursor_pos.y == yi:
                pygame.draw.rect(screen, '#ffffff', (x - 2, y, self.cell_size.x, self.cell_size.y - 4), 1, 8)

            if self.items[i].has_children():
                pass

            xi += 1
            x += self.cell_size.x

            if xi > self.table.x - 1:
                xi = 0
                x = offset.x + 10

                yi += 1
                y += self.cell_size.y

class MenuManager:
    def __init__(self):
        self.menus: list[MenuObject] = []
    
    def open_menu(self, menu):
        self.menus.append(menu)
    
    def close_menu(self):
        self.menus.pop()
    
    def close_all(self):
        self.menus.clear()

    def Navigate(self, dx, dy):
        if len(self.menus):
            self.menus[-1].Navigate(dx, dy)
    
    def Confirm(self):
        if not len(self.menus):
            return [None]
        
        ci = self.menus[-1].CursorItem()
        
        if ci.enabled:
            if ci.has_children():
                self.open_menu(ci)
            else:
                r = [c.CursorItem().name for c in self.menus]
                
                self.close_all()

                return r

        return [None]

    def Back(self):
        self.close_menu()

    def draw(self, screen, position):
        p = position.copy()

        for m in self.menus:
            m.draw(screen, p)
            p.x += 8
            p.y += 8