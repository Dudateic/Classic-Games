"""Tela de preparação – contagem regressiva 3-2-1 antes do nível."""
import time
import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color


class ReadyScreen:
    DURATION = 3.0

    def __init__(self, level: int) -> None:
        self._level   = level
        self._start   = time.time()
        self._font_lg = pygame.font.SysFont("monospace", 96, bold=True)
        self._font_sm = pygame.font.SysFont("monospace", 26, bold=True)
        self._font_md = pygame.font.SysFont("monospace", 20)

    def update(self) -> bool:
        """Retorna True enquanto deve ser exibida."""
        return (time.time() - self._start) < self.DURATION

    def draw(self, surface: pygame.Surface, session_draw_fn) -> None:
        session_draw_fn(surface)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        elapsed  = time.time() - self._start
        count    = 3 - int(elapsed)
        fraction = elapsed % 1.0

        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        lv_surf = self._font_sm.render(f"NÍVEL  {self._level}", True, Color.HUD_TEXT)
        surface.blit(lv_surf, (cx - lv_surf.get_width() // 2, cy - 120))

        if count > 0:
            scale = 1.0 + 0.5 * fraction
            alpha = int(255 * (1 - fraction ** 1.5))
            num_surf = self._font_lg.render(str(count), True, Color.BALL)
            num_surf = pygame.transform.scale(
                num_surf,
                (int(num_surf.get_width() * scale), int(num_surf.get_height() * scale))
            )
            num_surf.set_alpha(alpha)
            surface.blit(num_surf, (cx - num_surf.get_width() // 2, cy - num_surf.get_height() // 2))
        else:
            go_surf = self._font_lg.render("GO!", True, Color.GREEN)
            go_surf.set_alpha(int(255 * (1 - fraction)))
            surface.blit(go_surf, (cx - go_surf.get_width() // 2, cy - go_surf.get_height() // 2))

