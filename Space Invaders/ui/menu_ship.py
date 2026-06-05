import random


class MenuShip:

    def __init__(self, screen_width, screen_height, sprite):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sprite = sprite
        self._reset()

    def _reset(self):
        self.x = random.randint(0, self.screen_width - self.sprite.get_width())
        self.y = random.randint(-self.screen_height, 0)
        self.speed = random.uniform(0.5, 1.5)

    def move(self):
        self.y += self.speed
        if self.y > self.screen_height:
            self._reset()

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))


def make_menu_ships(screen_width, screen_height, sprite, count=5):
    return [MenuShip(screen_width, screen_height, sprite) for _ in range(count)]
