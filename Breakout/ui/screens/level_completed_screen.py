import time
import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color, TOTAL_LEVELS

"""Tela de nível concluído – mostra estatísticas e bônus."""

class LevelCompletedScreen:
    DURATION = 4.0

    def __init__(self, level: int, score: int, lives: int) -> None:
        self._level   = level
        self._score   = score
        self._lives   = lives
        self._start   = time.time()
        self._bonus   = lives * 50 + level * 25
        self._font_lg = pygame.font.SysFont("monospace", 52, bold=True)
        self._font_md = pygame.font.SysFont("monospace", 24, bold=True)
        self._font_sm = pygame.font.SysFont("monospace", 18)
        self._confirmed = False

    @property
    def bonus(self) -> int:
        return self._bonus

    def confirm(self) -> None:
        self._confirmed = True

    def is_done(self) -> bool:
        return self._confirmed or (time.time() - self._start) >= self.DURATION

    def draw(self, surface: pygame.Surface) -> None:
        elapsed = time.time() - self._start
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 190))
        surface.blit(overlay, (0, 0))

        title_color = Color.GREEN if self._level < TOTAL_LEVELS else Color.GOLD
        title_text  = f"NÍVEL {self._level} COMPLETO!" if self._level < TOTAL_LEVELS else "TODOS OS NÍVEIS!"
        t = self._font_lg.render(title_text, True, title_color)
        surface.blit(t, (cx - t.get_width() // 2, cy - 130))

        pygame.draw.line(surface, Color.GOLD, (cx - 200, cy - 80), (cx + 200, cy - 80), 2)

        rows = [
            ("Pontuação:   ", f"{self._score:,}",       Color.HUD_TEXT),
            ("Vidas restantes:", f"{self._lives}  × 50 = {self._lives*50:,} pts", (220, 180, 80)),
            ("Bônus de nível:", f"+{self._bonus:,} pts", Color.BALL),
        ]
        for i, (label, value, color) in enumerate(rows):
            y = cy - 50 + i * 38
            lsurf = self._font_sm.render(label, True, Color.HUD_TEXT)
            vsurf = self._font_md.render(value, True, color)
            surface.blit(lsurf, (cx - 220, y))
            surface.blit(vsurf, (cx + 20,  y - 3))

        pygame.draw.line(surface, Color.GOLD, (cx - 200, cy + 70), (cx + 200, cy + 70), 2)

        if self._level < TOTAL_LEVELS:
            next_text = f"Próximo: Nível {self._level + 1}"
            cont_text = "ESPAÇO  →  Comprar Upgrades"
        else:
            next_text = "Parabéns! Você zerou o jogo!"
            cont_text = "ESPAÇO  →  Ver Créditos"

        n = self._font_md.render(next_text, True, Color.WHITE)
        c = self._font_sm.render(cont_text, True, Color.HUD_TEXT)
        surface.blit(n, (cx - n.get_width() // 2, cy + 85))
        surface.blit(c, (cx - c.get_width() // 2, cy + 120))

        bar_w = int(300 * min(1.0, elapsed / self.DURATION))
        pygame.draw.rect(surface, (60, 60, 70), (cx - 150, cy + 155, 300, 6), border_radius=3)
        pygame.draw.rect(surface, Color.BALL,   (cx - 150, cy + 155, bar_w, 6), border_radius=3)
