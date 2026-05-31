from typing import List, Tuple
import pygame
from core.config import (
    BRICK_COLS, BRICK_ROWS, BRICK_WIDTH, BRICK_HEIGHT,
    BRICK_PADDING, BRICK_OFFSET_TOP, BRICK_OFFSET_LEFT,
)
from .brick import Brick


class BrickGrid:
    def __init__(self) -> None:
        self.bricks: List[Brick] = []
        self._build()

    def _build(self) -> None:
        self.bricks.clear()
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                y = BRICK_OFFSET_TOP  + row * (BRICK_HEIGHT + BRICK_PADDING)
                rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
                self.bricks.append(Brick(rect, row, BRICK_ROWS))

    def reset(self) -> None:
        self._build()

    @property
    def all_destroyed(self) -> bool:
        return all(not b.alive for b in self.bricks)

    def collide_ball(self, ball_rect: pygame.Rect) -> Tuple[int, bool, bool]:
        points = 0
        reflect_v = False
        reflect_h = False

        for brick in self.bricks:
            if not brick.alive:
                continue
            if not ball_rect.colliderect(brick.rect):
                continue

            dx = min(ball_rect.right  - brick.rect.left,
                     brick.rect.right - ball_rect.left)
            dy = min(ball_rect.bottom - brick.rect.top,
                     brick.rect.bottom - ball_rect.top)

            if dy <= dx:
                reflect_v = True
            else:
                reflect_h = True

            points += brick.destroy()

        return points, reflect_v, reflect_h

    def draw(self, surface: pygame.Surface) -> None:
        for brick in self.bricks:
            brick.draw(surface)
