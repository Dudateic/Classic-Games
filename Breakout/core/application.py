import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, Color
from core.state import GameState
from core.input_handler import InputHandler
from core.game_session import GameSession
from ui.hud import HUD
from utils.score_io import load_high_score, save_high_score


class Application:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(TITLE)
        self._screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock   = pygame.time.Clock()
        self._input   = InputHandler()
        self._session = GameSession()
        self._hud     = HUD()
        self._state   = GameState.MENU
        self._high_score = load_high_score()

    def run(self) -> None:
        running = True
        while running:
            snap = self._input.process()
            if snap.quit:
                break

            self._handle_global_keys(snap)
            self._update(snap)
            self._render()
            self._clock.tick(FPS)

        save_high_score(self._high_score)
        pygame.quit()

    def _handle_global_keys(self, snap) -> None:
        if pygame.K_ESCAPE in snap.keys_pressed:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self._state == GameState.PLAYING:
            if pygame.K_p in snap.keys_pressed:
                self._state = GameState.PAUSED
        elif self._state == GameState.PAUSED:
            if pygame.K_p in snap.keys_pressed or pygame.K_SPACE in snap.keys_pressed:
                self._state = GameState.PLAYING

    def _update(self, snap) -> None:
        if self._state == GameState.MENU:
            if pygame.K_SPACE in snap.keys_pressed:
                self._session.full_reset()
                self._state = GameState.PLAYING

        elif self._state == GameState.PLAYING:
            next_state = self._session.update(snap)
            if next_state in (GameState.GAME_OVER, GameState.VICTORY):
                self._high_score = max(self._high_score, self._session.score)
                self._state = next_state

        elif self._state in (GameState.GAME_OVER, GameState.VICTORY):
            if pygame.K_SPACE in snap.keys_pressed:
                self._session.full_reset()
                self._state = GameState.PLAYING

    def _render(self) -> None:
        self._screen.fill(Color.GRAY)

        pygame.draw.line(self._screen, (50, 50, 60), (0, 32), (SCREEN_WIDTH, 32))

        if self._state == GameState.PLAYING or self._state == GameState.PAUSED:
            self._session.draw(self._screen)

        self._hud.draw(
            self._screen,
            self._state,
            self._session.score,
            self._session.lives,
            self._high_score,
        )

        pygame.display.flip()
