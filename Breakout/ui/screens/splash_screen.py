import pygame
import time
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color

"""Splash screen – breve tela de abertura do estúdio."""

class SplashScreen:
    DURATION = 2.5

    def __init__(self) -> None:
        self._font_title = pygame.font.SysFont("monospace", 36, bold=True)
        self._font_sub   = pygame.font.SysFont("monospace", 16)
        self._start      = time.time()

    def update(self) -> bool:
        """Retorna True enquanto deve ser exibida."""
        return (time.time() - self._start) < self.DURATION

    def draw(self, surface: pygame.Surface) -> None:
        elapsed  = time.time() - self._start
        progress = elapsed / self.DURATION

        if progress < 0.3:
            alpha = int(255 * (progress / 0.3))
        elif progress > 0.75:
            alpha = int(255 * (1 - (progress - 0.75) / 0.25))
        else:
            alpha = 255

        surface.fill(Color.GRAY)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        title_surf = self._font_title.render("BREAKOUT", True, Color.BALL)
        sub_surf   = self._font_sub.render("presents", True, Color.HUD_TEXT)

        title_surf.set_alpha(alpha)
        sub_surf.set_alpha(alpha)

        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2

        line_w = int(300 * min(1.0, progress / 0.4))
        pygame.draw.line(surface, (*Color.BALL, alpha),
                         (cx - line_w // 2, cy - 50),
                         (cx + line_w // 2, cy - 50), 2)

        surface.blit(title_surf, (cx - title_surf.get_width() // 2, cy - 20))
        surface.blit(sub_surf,   (cx - sub_surf.get_width()  // 2, cy + 30))

        pygame.draw.line(surface, (*Color.BALL, alpha),
                         (cx - line_w // 2, cy + 55),
                         (cx + line_w // 2, cy + 55), 2)
