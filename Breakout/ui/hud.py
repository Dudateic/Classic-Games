import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, Color
from core.state import GameState


class HUD:
    def __init__(self) -> None:
        self._font_sm  = pygame.font.SysFont("monospace", 18, bold=True)
        self._font_lg  = pygame.font.SysFont("monospace", 48, bold=True)
        self._font_med = pygame.font.SysFont("monospace", 26, bold=True)

    def draw(self, surface: pygame.Surface, state: GameState,
             score: int, lives: int, high_score: int) -> None:
        self._draw_stats(surface, score, lives, high_score)

        if state == GameState.MENU:
            self._draw_centered(surface, "BREAKOUT",  self._font_lg,  Color.BALL, -80)
            self._draw_centered(surface, "PRESSIONE ESPAÇO PARA JOGAR",
                                self._font_med, Color.HUD_TEXT, 10)

        elif state == GameState.PAUSED:
            self._draw_overlay(surface)
            self._draw_centered(surface, "PAUSADO",  self._font_lg,  Color.BALL, -40)
            self._draw_centered(surface, "ESPAÇO para continuar",
                                self._font_med, Color.HUD_TEXT, 30)

        elif state == GameState.GAME_OVER:
            self._draw_overlay(surface)
            self._draw_centered(surface, "GAME OVER", self._font_lg, (220, 60, 60), -60)
            self._draw_centered(surface, f"Pontuação: {score}",
                                self._font_med, Color.HUD_TEXT, 10)
            self._draw_centered(surface, "ESPAÇO para reiniciar",
                                self._font_sm, Color.HUD_TEXT, 50)

        elif state == GameState.VICTORY:
            self._draw_overlay(surface)
            self._draw_centered(surface, "VOCÊ VENCEU!", self._font_lg, (60, 220, 80), -60)
            self._draw_centered(surface, f"Pontuação final: {score}",
                                self._font_med, Color.HUD_TEXT, 10)
            self._draw_centered(surface, "ESPAÇO para jogar novamente",
                                self._font_sm, Color.HUD_TEXT, 50)

        elif state == GameState.PLAYING:
            self._draw_centered(surface, "ESPAÇO para lançar · P para pausar",
                                self._font_sm, Color.GRAY, SCREEN_HEIGHT // 2 - 20,
                                y_absolute=True)

    def _draw_stats(self, surface: pygame.Surface,
                    score: int, lives: int, high_score: int) -> None:
        score_surf = self._font_sm.render(f"SCORE  {score:06d}", True, Color.HUD_TEXT)
        hi_surf    = self._font_sm.render(f"BEST   {high_score:06d}", True, Color.HUD_TEXT)
        lives_surf = self._font_sm.render(f"VIDAS  {'♥ ' * lives}", True, (220, 80, 80))

        surface.blit(score_surf, (14, 8))
        hi_surf_x = SCREEN_WIDTH // 2 - hi_surf.get_width() // 2
        surface.blit(hi_surf, (hi_surf_x, 8))
        lives_x = SCREEN_WIDTH - lives_surf.get_width() - 14
        surface.blit(lives_surf, (lives_x, 8))

    def _draw_centered(self, surface: pygame.Surface, text: str,
                       font: pygame.font.Font, color: tuple,
                       y_offset: int, y_absolute: bool = False) -> None:
        surf = font.render(text, True, color)
        x = (SCREEN_WIDTH  - surf.get_width())  // 2
        y = y_offset if y_absolute else (SCREEN_HEIGHT // 2 + y_offset)
        surface.blit(surf, (x, y))

    def _draw_overlay(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))
