import time
import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color

"""Tela de créditos – exibida após vencer todos os níveis."""

_CREDITS = [
    ("BREAKOUT", "title"),
    ("", "gap"),
    ("Desenvolvido com", "label"),
    ("Python  &  Pygame", "value"),
    ("", "gap"),
    ("Código & Design", "label"),
    ("BREAKOUT", "value"),
    ("", "gap"),
    ("Tecnologias Utilizadas", "label"),
    ("pygame-ce 2.x", "value"),
    ("Python 3.11+", "value"),
    ("", "gap"),
    ("Obrigado por jogar!", "label"),
    ("Pressione ESPAÇO para o Menu", "cta"),
]

SCROLL_SPEED = 40


class CreditsScreen:
    def __init__(self, score: int) -> None:
        self._score    = score
        self._start    = time.time()
        self._done     = False
        self._scroll_y = SCREEN_HEIGHT + 20
        self._font_title = pygame.font.SysFont("monospace", 56, bold=True)
        self._font_label = pygame.font.SysFont("monospace", 18)
        self._font_value = pygame.font.SysFont("monospace", 24, bold=True)
        self._font_cta   = pygame.font.SysFont("monospace", 20, bold=True)

    @property
    def done(self) -> bool:
        return self._done

    def handle_key(self, key: int) -> None:
        if key in (pygame.K_SPACE, pygame.K_ESCAPE):
            self._done = True

    def update(self) -> None:
        dt = 1 / 60
        self._scroll_y -= SCROLL_SPEED * dt

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((10, 10, 20))

        cx = SCREEN_WIDTH // 2
        y  = self._scroll_y

        for text, kind in _CREDITS:
            if kind == "gap":
                y += 30
                continue

            if kind == "title":
                font  = self._font_title
                color = Color.BALL
            elif kind == "label":
                font  = self._font_label
                color = Color.HUD_TEXT
            elif kind == "value":
                font  = self._font_value
                color = Color.WHITE
            elif kind == "cta":
                font  = self._font_cta
                pulse = abs((time.time() * 2) % 2 - 1)
                color = tuple(int(c + (255 - c) * pulse * 0.3) for c in Color.BALL)
            else:
                font  = self._font_label
                color = Color.HUD_TEXT

            surf = font.render(text, True, color)
            surface.blit(surf, (cx - surf.get_width() // 2, int(y)))
            y += surf.get_height() + 10

        if y < SCREEN_HEIGHT - 80:
            sc_font = self._font_value
            sc_surf = sc_font.render(f"Pontuação final:  {self._score:,}", True, Color.GOLD)
            surface.blit(sc_surf, (cx - sc_surf.get_width() // 2, SCREEN_HEIGHT - 70))

        for edge_y, flip in ((0, False), (SCREEN_HEIGHT - 60, True)):
            grad = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
            for i in range(60):
                alpha = int(255 * (i / 60)) if flip else int(255 * (1 - i / 60))
                pygame.draw.line(grad, (10, 10, 20, alpha), (0, i), (SCREEN_WIDTH, i))
            surface.blit(grad, (0, edge_y))
