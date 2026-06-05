import pygame


class Spell:

    WIDTH = 5
    HEIGHT = 15
    SPEED = 8
    COLOR = (255, 255, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= self.SPEED

    def off_screen(self):
        return self.y < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))
