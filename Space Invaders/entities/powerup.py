import random
import pygame


POWERUP_TYPES = ("shield", "double", "laser")
POWERUP_COLOR = (0, 255, 255)
POWERUP_SIZE = 20
POWERUP_SPEED = 2


class PowerUp:

    def __init__(self, x, y, kind=None):
        self.x = x
        self.y = y
        self.kind = kind or random.choice(POWERUP_TYPES)

    def move(self):
        self.y += POWERUP_SPEED

    def off_screen(self, height):
        return self.y > height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, POWERUP_SIZE, POWERUP_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, POWERUP_COLOR, (self.x, self.y, POWERUP_SIZE, POWERUP_SIZE))
        label_font = pygame.font.SysFont("Arial", 10, bold=True)
        label = label_font.render(self.kind[0].upper(), True, (0, 0, 0))
        screen.blit(label, (self.x + 4, self.y + 5))
