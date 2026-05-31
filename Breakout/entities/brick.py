import pygame
from core.config import Color


class Brick:

    def __init__(self, rect: pygame.Rect, row: int, total_rows: int) -> None:
        self.rect      = rect
        self.alive     = True
        self.color     = Color.BRICK_ROWS[row % len(Color.BRICK_ROWS)]
        self.points    = (total_rows - row) * 10

    def destroy(self) -> int:
        self.alive = False
        return self.points

    def draw(self, surface: pygame.Surface) -> None:
        if not self.alive:
            return
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        # Borda interna
        pygame.draw.rect(surface, Color.GRAY, self.rect, width=1, border_radius=4)
