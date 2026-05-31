import math
import pygame
from core.config import (
    BALL_RADIUS, BALL_SPEED_INIT, BALL_SPEED_MAX, BALL_SPEED_INC,
    SCREEN_WIDTH, SCREEN_HEIGHT, Color,
)


class Ball:

    def __init__(self) -> None:
        self._speed = BALL_SPEED_INIT
        self.radius = BALL_RADIUS
        self.rect = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self._vx = 0.0
        self._vy = 0.0
        self._active = False   # aguarda lançamento pelo jogador

    def reset(self, paddle_rect: pygame.Rect) -> None:
        self._speed  = BALL_SPEED_INIT
        self._active = False
        self.rect.centerx = paddle_rect.centerx
        self.rect.bottom   = paddle_rect.top - 2
        self._vx = self._speed
        self._vy = -self._speed

    def launch(self) -> None:
        if not self._active:
            self._active = True

    @property
    def active(self) -> bool:
        return self._active

    def update(self, paddle_rect: pygame.Rect) -> bool:
        if not self._active:
            self.rect.centerx = paddle_rect.centerx
            self.rect.bottom   = paddle_rect.top - 2
            return True

        self.rect.x += self._vx
        self.rect.y += self._vy

        if self.rect.left <= 0:
            self.rect.left = 0
            self._vx = abs(self._vx)
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self._vx = -abs(self._vx)

        # Teto
        if self.rect.top <= 0:
            self.rect.top = 0
            self._vy = abs(self._vy)

        # Paddle
        if self.rect.colliderect(paddle_rect) and self._vy > 0:
            self._reflect_off_paddle(paddle_rect)

        if self.rect.top > SCREEN_HEIGHT:
            return False

        return True

    def _reflect_off_paddle(self, paddle_rect: pygame.Rect) -> None:

        relative = (self.rect.centerx - paddle_rect.left) / paddle_rect.width  # [0, 1]
        angle_deg = 20 + (relative * 140)   # 20° 160°
        angle_rad = math.radians(angle_deg)

        self._vx = self._speed * math.cos(math.radians(angle_deg - 90))
        self._vy = -abs(self._speed * math.sin(math.radians(angle_deg - 90)))
        self.rect.bottom = paddle_rect.top - 1

    def reflect_vertical(self) -> None:
        self._vy = -self._vy

    def reflect_horizontal(self) -> None:
        self._vx = -self._vx

    def increase_speed(self) -> None:
        self._speed = min(self._speed + BALL_SPEED_INC, BALL_SPEED_MAX)
        magnitude = math.hypot(self._vx, self._vy)
        if magnitude:
            factor = self._speed / magnitude
            self._vx *= factor
            self._vy *= factor

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, Color.BALL, self.rect.center, self.radius)
        pygame.draw.circle(surface, Color.WHITE,
                           (self.rect.centerx - 2, self.rect.centery - 2), 2)
