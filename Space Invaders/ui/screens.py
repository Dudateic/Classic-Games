"""
Screen renderers for every non-gameplay state.

Each function receives `screen` and whatever data it needs to display,
and draws directly — no state is stored here.
"""

import pygame
from ui.starfield import draw_starfield


_BG_COLOR     = (0, 0, 20)
_GOLD         = (255, 215, 0)
_WHITE        = (255, 255, 255)
_YELLOW       = (255, 255, 0)
_HINT         = (200, 200, 255)
_SHADOW       = (50, 50, 50)
_ENTRY_BG     = (0, 0, 50)


def _shadow_blit(screen, font, text, color, x, y, shadow_color=_SHADOW, offset=4):
    shadow = font.render(text, True, shadow_color)
    surface = font.render(text, True, color)
    screen.blit(shadow, (x + offset, y + offset))
    screen.blit(surface, (x, y))


def _centered_x(screen, surface):
    return screen.get_width() // 2 - surface.get_width() // 2



class MenuScreen:
    """Interactive menu: navigates options with move_up / move_down."""

    OPTIONS = ["START", "RANKING", "SAIR"]

    _TITLE_FONT_SIZE  = 64
    _OPTION_FONT_SIZE = 36
    _OPTION_START_Y   = 250
    _OPTION_SPACING   = 60

    def __init__(self):
        self.selected = 0

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.OPTIONS)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.OPTIONS)

    def get_selected(self):
        return self.OPTIONS[self.selected]

    def draw(self, screen, stars):
        screen.fill(_BG_COLOR)
        draw_starfield(screen, stars)

        title_font  = pygame.font.SysFont("Arial", self._TITLE_FONT_SIZE, bold=True)
        option_font = pygame.font.SysFont("Arial", self._OPTION_FONT_SIZE, bold=True)

        # title
        title = title_font.render("DEFESA DA GALÁXIA", True, _GOLD)
        _shadow_blit(screen, title_font, "DEFESA DA GALÁXIA", _GOLD,
                     _centered_x(screen, title), 100)

        # options
        for i, option in enumerate(self.OPTIONS):
            color = _YELLOW if i == self.selected else _WHITE
            surf = option_font.render(option, True, color)
            y = self._OPTION_START_Y + i * self._OPTION_SPACING

            if i == self.selected:
                bg = pygame.Surface((surf.get_width() + 20, surf.get_height() + 10))
                bg.fill(_YELLOW)
                bg.set_alpha(80)
                screen.blit(bg, (_centered_x(screen, bg), y - 5))

            screen.blit(surf, (_centered_x(screen, surf), y))



def draw_name_input(screen, stars, player_name):
    screen.fill(_BG_COLOR)
    draw_starfield(screen, stars)

    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    _shadow_blit(screen, title_font, "Digite seu nome", _WHITE,
                 _centered_x(screen, title_font.render("Digite seu nome", True, _WHITE)), 150)

    input_font = pygame.font.SysFont("Arial", 36, bold=True)
    display = player_name if player_name else "_"
    input_surf = input_font.render(display, True, _YELLOW)

    bg = pygame.Surface((input_surf.get_width() + 20, input_surf.get_height() + 10))
    bg.fill(_WHITE)
    bg.set_alpha(50)
    ix = _centered_x(screen, bg)
    iy = 250
    screen.blit(bg, (ix, iy))
    screen.blit(input_surf, (ix + 10, iy + 5))

    hint_font = pygame.font.SysFont("Arial", 24)
    hint = hint_font.render("Pressione ENTER para continuar", True, _HINT)
    screen.blit(hint, (_centered_x(screen, hint), iy + 70))



def draw_start_screen(screen, stars, player_name):
    screen.fill(_BG_COLOR)
    draw_starfield(screen, stars)

    welcome_font = pygame.font.SysFont("Arial", 48, bold=True)
    welcome = welcome_font.render(f"Bem-vindo, {player_name}!", True, _WHITE)
    screen.blit(welcome, (_centered_x(screen, welcome), 250))

    start_font = pygame.font.SysFont("Arial", 36, bold=True)
    start = start_font.render("Pressione ENTER para começar", True, _YELLOW)
    screen.blit(start, (_centered_x(screen, start), 330))



def draw_ranking_screen(screen, stars, ranking_data):
    screen.fill(_BG_COLOR)
    draw_starfield(screen, stars)

    title_font  = pygame.font.SysFont("Arial", 64, bold=True)
    entry_font  = pygame.font.SysFont("Arial", 36, bold=True)
    hint_font   = pygame.font.SysFont("Arial", 24)

    title = title_font.render("TOP 10 JOGADORES", True, _GOLD)
    _shadow_blit(screen, title_font, "TOP 10 JOGADORES", _GOLD,
                 _centered_x(screen, title), 50)

    start_y, spacing = 150, 50
    for i, player in enumerate(ranking_data):
        text = entry_font.render(f"{i+1}. {player['name']} — {player['score']}", True, _WHITE)
        bg = pygame.Surface((text.get_width() + 20, text.get_height() + 10))
        bg.fill(_ENTRY_BG)
        bg.set_alpha(120)
        bx = _centered_x(screen, bg)
        by = start_y + i * spacing
        screen.blit(bg, (bx, by))
        screen.blit(text, (_centered_x(screen, text), by + 5))

    hint = hint_font.render("Pressione ESC para voltar", True, _HINT)
    screen.blit(hint, (_centered_x(screen, hint), start_y + len(ranking_data) * spacing + 30))



def draw_game_over(screen, score):
    sw, sh = screen.get_width(), screen.get_height()

    overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    title_font  = pygame.font.SysFont("Arial", 72, bold=True)
    body_font   = pygame.font.SysFont("Arial", 32)
    hint_font   = pygame.font.SysFont("Arial", 24)

    title = title_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(title, (_centered_x(screen, title), sh // 2 - 130))

    score_surf = body_font.render(f"Pontuação: {score}", True, _WHITE)
    screen.blit(score_surf, (_centered_x(screen, score_surf), sh // 2 - 40))

    for i, line in enumerate(["ENTER — Recomeçar", "ESC — Menu"]):
        hint = hint_font.render(line, True, _HINT)
        screen.blit(hint, (_centered_x(screen, hint), sh // 2 + 20 + i * 35))
