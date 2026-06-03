import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color
from utils.score_io import load_scores

"""Tela de ranking – exibe top 5 pontuações locais."""

class HighScoresScreen:
    def __init__(self) -> None:
        self._scores   = load_scores()
        self._done     = False
        self._font_lg  = pygame.font.SysFont("monospace", 40, bold=True)
        self._font_md  = pygame.font.SysFont("monospace", 24, bold=True)
        self._font_sm  = pygame.font.SysFont("monospace", 18)
        self._font_xs  = pygame.font.SysFont("monospace", 14)
        self._medals   = ["🥇", "🥈", "🥉", " 4.", " 5."]

    @property
    def done(self) -> bool:
        return self._done

    def handle_key(self, key: int) -> None:
        if key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_BACKSPACE):
            self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(Color.GRAY)
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        # Título
        t = self._font_lg.render("TOP 5  PONTUAÇÕES", True, Color.GOLD)
        surface.blit(t, (cx - t.get_width() // 2, 35))
        pygame.draw.line(surface, Color.GOLD, (cx - 220, 95), (cx + 220, 95), 2)

        if not self._scores:
            ns = self._font_md.render("Nenhum recorde ainda. Jogue mais!", True, Color.HUD_TEXT)
            surface.blit(ns, (cx - ns.get_width() // 2, cy))
        else:
            row_colors = [
                Color.GOLD,
                (192, 192, 192),
                (205, 127, 50),
                Color.HUD_TEXT,
                Color.HUD_TEXT,
            ]
            row_h   = 70
            start_y = 115

            for i, entry in enumerate(self._scores[:5]):
                y   = start_y + i * row_h
                col = row_colors[i]

                rect = pygame.Rect(80, y, SCREEN_WIDTH - 160, 55)
                bg   = (50, 50, 70) if i % 2 == 0 else (40, 40, 60)
                pygame.draw.rect(surface, bg, rect, border_radius=6)

                medal = self._medals[i]
                ms = self._font_md.render(medal, True, col)
                surface.blit(ms, (rect.x + 14, rect.y + 12))

                name = entry.get("name", "---")[:6].upper()
                ns   = self._font_md.render(name, True, Color.WHITE)
                surface.blit(ns, (rect.x + 70, rect.y + 12))

                lv_text = f"Nív. {entry.get('level', 1)}"
                ls = self._font_sm.render(lv_text, True, Color.HUD_TEXT)
                surface.blit(ls, (rect.x + 200, rect.y + 17))

                sc_text = f"{entry['score']:,}"
                ss = self._font_md.render(sc_text, True, col)
                surface.blit(ss, (rect.right - ss.get_width() - 16, rect.y + 12))

        hint = self._font_xs.render("ESPAÇO ou ESC para voltar", True, (100, 100, 120))
        surface.blit(hint, (cx - hint.get_width() // 2, SCREEN_HEIGHT - 40))
