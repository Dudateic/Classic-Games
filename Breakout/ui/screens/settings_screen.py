import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color

"""Tela de configurações – sensibilidade do mouse, modo de exibição, volume."""

class SettingsScreen:
    defaults = {
        "mouse_sensitivity": 2,
        "fullscreen": False,
        "sfx_volume": 2,
    }

    def __init__(self, current: dict) -> None:
        self._cfg      = dict(current)
        self._selected = 0
        self._done     = False
        self._font_lg  = pygame.font.SysFont("monospace", 40, bold=True)
        self._font_md  = pygame.font.SysFont("monospace", 22, bold=True)
        self._font_sm  = pygame.font.SysFont("monospace", 17)
        self._font_xs  = pygame.font.SysFont("monospace", 14)

        self._options = [
            {
                "key":    "mouse_sensitivity",
                "label":  "Sensibilidade do Mouse",
                "values": [1, 2, 3],
                "names":  ["Baixa", "Média", "Alta"],
            },
            {
                "key":    "sfx_volume",
                "label":  "Volume de Efeitos",
                "values": [0, 1, 2, 3],
                "names":  ["Mudo", "Baixo", "Médio", "Alto"],
            },
            {
                "key":    "fullscreen",
                "label":  "Modo Tela Cheia",
                "values": [False, True],
                "names":  ["Desativado", "Ativado"],
            },
        ]

    @property
    def done(self) -> bool:
        return self._done

    @property
    def config(self) -> dict:
        return self._cfg

    def handle_key(self, key: int) -> None:
        if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self._done = True
        elif key == pygame.K_UP:
            self._selected = (self._selected - 1) % len(self._options)
        elif key == pygame.K_DOWN:
            self._selected = (self._selected + 1) % len(self._options)
        elif key in (pygame.K_LEFT, pygame.K_RIGHT):
            opt = self._options[self._selected]
            vals = opt["values"]
            cur_idx = vals.index(self._cfg.get(opt["key"], vals[0]))
            if key == pygame.K_RIGHT:
                new_idx = (cur_idx + 1) % len(vals)
            else:
                new_idx = (cur_idx - 1) % len(vals)
            self._cfg[opt["key"]] = vals[new_idx]

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(Color.GRAY)
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        t = self._font_lg.render("CONFIGURAÇÕES", True, Color.BALL)
        surface.blit(t, (cx - t.get_width() // 2, 40))
        pygame.draw.line(surface, (60, 60, 80), (80, 100), (SCREEN_WIDTH - 80, 100), 1)

        row_h   = 80
        start_y = cy - (len(self._options) * row_h) // 2

        for i, opt in enumerate(self._options):
            y       = start_y + i * row_h
            is_sel  = (i == self._selected)
            rect    = pygame.Rect(80, y, SCREEN_WIDTH - 160, 60)
            bg      = (50, 50, 70) if not is_sel else (70, 70, 100)
            pygame.draw.rect(surface, bg, rect, border_radius=8)
            if is_sel:
                pygame.draw.rect(surface, Color.BALL, rect, width=2, border_radius=8)

            ls = self._font_md.render(opt["label"], True, Color.WHITE if is_sel else Color.HUD_TEXT)
            surface.blit(ls, (rect.x + 20, rect.y + 15))

            vals    = opt["values"]
            cur_idx = vals.index(self._cfg.get(opt["key"], vals[0]))
            val_str = f"◄  {opt['names'][cur_idx]}  ►"
            vs = self._font_sm.render(val_str, True, Color.GOLD if is_sel else Color.HUD_TEXT)
            surface.blit(vs, (rect.right - vs.get_width() - 20, rect.y + 18))

