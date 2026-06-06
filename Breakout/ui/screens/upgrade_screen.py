import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color, UPGRADES

"""Tela de loja de upgrades entre níveis."""

class UpgradeScreen:
    def __init__(self, score: int) -> None:
        self._score        = score
        self._selected     = 0
        self._purchased    = set()
        self._font_lg      = pygame.font.SysFont("monospace", 40, bold=True)
        self._font_md      = pygame.font.SysFont("monospace", 22, bold=True)
        self._font_sm      = pygame.font.SysFont("monospace", 17)
        self._font_xs      = pygame.font.SysFont("monospace", 14)
        self._done         = False
        self._message      = ""
        self._msg_timer    = 0

    @property
    def done(self) -> bool:
        return self._done

    @property
    def purchased(self) -> set:
        return self._purchased

    def update_score(self, score: int) -> None:
        self._score = score

    def handle_key(self, key: int, session) -> None:
        if key == pygame.K_UP:
            self._selected = (self._selected - 1) % len(UPGRADES)
        elif key == pygame.K_DOWN:
            self._selected = (self._selected + 1) % len(UPGRADES)
        elif key in (pygame.K_RETURN, pygame.K_z):
            self._buy(self._selected, session)
        elif key in (pygame.K_SPACE, pygame.K_ESCAPE):
            self._done = True

    def _buy(self, idx: int, session) -> None:
        upgrade = UPGRADES[idx]
        if upgrade["id"] in self._purchased:
            self._set_msg("Já comprado!", Color.RED)
            return
        ok = session.apply_upgrade(upgrade["id"])
        if ok:
            self._purchased.add(upgrade["id"])
            self._score = session.score
            self._set_msg(f"✓ {upgrade['label']} ativado!", Color.GREEN)
        else:
            self._set_msg("Pontos insuficientes!", Color.RED)

    def _set_msg(self, text: str, color: tuple) -> None:
        self._message = (text, color)
        self._msg_timer = 120

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(Color.GRAY)

        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2

        t = self._font_lg.render("LOJA DE UPGRADES", True, Color.BALL)
        surface.blit(t, (cx - t.get_width() // 2, 30))

        s = self._font_md.render(f"Pontos disponíveis:  {self._score:,}", True, Color.GOLD)
        surface.blit(s, (cx - s.get_width() // 2, 85))

        pygame.draw.line(surface, (60, 60, 80), (80, 115), (SCREEN_WIDTH - 80, 115), 1)

        card_h  = 80
        gap     = 12
        total_h = len(UPGRADES) * (card_h + gap)
        start_y = cy - total_h // 2

        for i, upg in enumerate(UPGRADES):
            y         = start_y + i * (card_h + gap)
            rect      = pygame.Rect(80, y, SCREEN_WIDTH - 160, card_h)
            is_sel    = (i == self._selected)
            bought    = upg["id"] in self._purchased
            can_buy   = self._score >= upg["cost"] and not bought

            bg_color = (50, 50, 70) if not is_sel else (70, 70, 100)
            if bought:
                bg_color = (30, 60, 30)
            pygame.draw.rect(surface, bg_color, rect, border_radius=8)
            border_col = Color.BALL if is_sel else (80, 80, 100)
            pygame.draw.rect(surface, border_col, rect, width=2, border_radius=8)

            icon_surf = self._font_lg.render(upg["icon"], True, Color.BALL if can_buy else (120, 120, 120))
            surface.blit(icon_surf, (rect.x + 16, rect.y + card_h // 2 - icon_surf.get_height() // 2))

            name_color = Color.WHITE if can_buy or bought else (140, 140, 140)
            n = self._font_md.render(upg["label"], True, name_color)
            d = self._font_xs.render(upg["desc"], True, Color.HUD_TEXT)
            surface.blit(n, (rect.x + 72, rect.y + 16))
            surface.blit(d, (rect.x + 72, rect.y + 44))

            if bought:
                cs = self._font_sm.render("COMPRADO", True, Color.GREEN)
            else:
                cost_color = Color.GOLD if can_buy else Color.RED
                cs = self._font_sm.render(f"{upg['cost']:,} pts", True, cost_color)
            surface.blit(cs, (rect.right - cs.get_width() - 16, rect.y + card_h // 2 - cs.get_height() // 2))

        if self._msg_timer > 0:
            self._msg_timer -= 1
            text, color = self._message
            ms = self._font_sm.render(text, True, color)
            surface.blit(ms, (cx - ms.get_width() // 2, SCREEN_HEIGHT - 80))
