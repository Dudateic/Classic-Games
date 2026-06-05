import math
import pygame


class EnemyShot:

    RADIUS = 5
    COLOR = (255, 0, 0)

    def __init__(self, x, y, target_x, target_y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed

        dist = math.hypot(target_x - x, target_y - y) or 1
        self.vx = (target_x - x) / dist * speed
        self.vy = (target_y - y) / dist * speed

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def off_screen(self, height):
        return self.y > height or self.y < 0

    def get_rect(self):
        r = self.RADIUS
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (int(self.x), int(self.y)), self.RADIUS)
