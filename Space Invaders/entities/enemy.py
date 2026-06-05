import pygame


class Enemy:

    def __init__(self, x, y, sprite, strategy, hp, points):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.strategy = strategy
        self.hp = hp
        self.max_hp = hp
        self.points = points

    def move(self):
        self.strategy.move(self)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
