import pygame


class Player:

    def __init__(self, sprite):
        self.sprite = sprite
        self.x = 400
        self.y = 500
        self.speed = 5

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(0, min(self.x, screen_width - self.sprite.get_width()))
        self.y = max(0, min(self.y, screen_height - self.sprite.get_height()))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
