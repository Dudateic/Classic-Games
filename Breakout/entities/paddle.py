import pygame
from core.config import (
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, PADDLE_Y,
    SCREEN_WIDTH, Color,
)


class Paddle:
    def __init__(self) -> None:
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
            PADDLE_Y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )

    def reset(self) -> None:
        self.rect.centerx = SCREEN_WIDTH // 2

    def update(self, input_snapshot) -> None:
        snap = input_snapshot

        if pygame.K_LEFT  in snap.keys_down: self.rect.x -= PADDLE_SPEED
        if pygame.K_RIGHT in snap.keys_down: self.rect.x += PADDLE_SPEED

        # Mouse tem prioridade se estiver se movendo
        self.rect.centerx = snap.mouse_x

        # Limita às bordas
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_WIDTH))
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, Color.PADDLE, self.rect, border_radius=6)
        # Highlight superior
        highlight = pygame.Rect(self.rect.x + 4, self.rect.y + 2, self.rect.width - 8, 3)
        pygame.draw.rect(surface, Color.WHITE, highlight, border_radius=2)
