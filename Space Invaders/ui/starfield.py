import random
import pygame


class Star:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset(randomize_y=True)

    def reset(self, randomize_y=False):
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height) if randomize_y else 0
        self.speed = random.randint(1, 4)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > self.height:
            self.reset()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size)


def make_starfield(width, height, count=50):
    return [Star(width, height) for _ in range(count)]


def draw_starfield(screen, stars):
    for star in stars:
        star.move()
        star.draw(screen)
