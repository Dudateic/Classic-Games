from typing import List, Tuple, Optional
import pygame
from core.config import (
    BRICK_COLS, BRICK_ROWS as BRICK_ROW_COUNT, BRICK_WIDTH, BRICK_HEIGHT,
    BRICK_PADDING, BRICK_OFFSET_TOP, BRICK_OFFSET_LEFT, Color,
)
from entities.brick import Brick
from levels.level_loader import get_layout


class BrickGrid:
    def __init__(self) -> None:
        self.bricks: List[Brick] = []
        self._level = 1
        self._build()

    def _build(self) -> None:
        self.bricks.clear()
        layout = get_layout(self._level)

        for row in range(BRICK_ROW_COUNT):
            for col in range(BRICK_COLS):
                x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                y = BRICK_OFFSET_TOP  + row * (BRICK_HEIGHT + BRICK_PADDING)
                rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

                if layout is not None:
                    cell = layout[row][col]
                    if cell == 0:
                        continue
                    hp = 1
                    if cell == 9:   hp = 2
                    elif cell == 8: hp = 3
                    color_row = (row % len(Color.BRICK_ROWS)) if cell in (8, 9) else (cell - 1) % len(Color.BRICK_ROWS)
                    brick = Brick(rect, color_row, BRICK_ROW_COUNT, hp)
                else:
                    brick = Brick(rect, row, BRICK_ROW_COUNT)
                self.bricks.append(brick)

    def set_level(self, level: int) -> None:
        self._level = level
        self._build()

    def reset(self) -> None:
        self._build()

    @property
    def all_destroyed(self) -> bool:
        return all(not b.alive for b in self.bricks)

    def collide_ball(self, ball_rect: pygame.Rect) -> Tuple[int, bool, bool, Optional[Tuple]]:
        """Retorna (points, reflect_v, reflect_h, hit_color)."""
        points = 0
        reflect_v = False
        reflect_h = False
        hit_color = None

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

            hit_color = brick.color
            pts = brick.hit()
            points += pts

        return points, reflect_v, reflect_h, hit_color

    def draw(self, surface: pygame.Surface) -> None:
        for brick in self.bricks:
            brick.draw(surface)
