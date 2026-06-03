import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, Color, TOTAL_LEVELS
from core.state import GameState
from core.input_handler import InputHandler
from core.game_session import GameSession
from ui.hud import HUD
from utils.score_io import load_high_score, add_score

from ui.screens.splash_screen          import SplashScreen
from ui.screens.ready_screen           import ReadyScreen
from ui.screens.level_completed_screen import LevelCompletedScreen
from ui.screens.upgrade_screen         import UpgradeScreen
from ui.screens.settings_screen        import SettingsScreen
from ui.screens.high_scores_screen     import HighScoresScreen
from ui.screens.credits_screen         import CreditsScreen


class Application:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(TITLE)
        self._screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock   = pygame.time.Clock()
        self._input   = InputHandler()
        self._session = GameSession()
        self._hud     = HUD()

        self._state      = GameState.SPLASH
        self._high_score = load_high_score()
        self._settings   = dict(SettingsScreen.defaults)

        self._splash          : SplashScreen           | None = SplashScreen()
        self._ready           : ReadyScreen             | None = None
        self._lc              : LevelCompletedScreen    | None = None
        self._upgrade         : UpgradeScreen           | None = None
        self._settings_screen : SettingsScreen          | None = None
        self._hiscores        : HighScoresScreen        | None = None
        self._credits         : CreditsScreen           | None = None

    def run(self) -> None:
        running = True
        while running:
            snap = self._input.process()
            if snap.quit:
                break

            for key in snap.keys_pressed:
                self._handle_key(key)

            self._update(snap)
            self._render()
            self._clock.tick(FPS)

        add_score(self._session.score, self._session.level)
        pygame.quit()

    def _handle_key(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            if self._state == GameState.PLAYING:
                self._state = GameState.PAUSED
            elif self._state in (GameState.PAUSED, GameState.SETTINGS, GameState.HIGH_SCORES):
                self._state = GameState.MENU
            else:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if self._state == GameState.MENU:
            if key == pygame.K_SPACE:
                self._begin_game()
            elif key == pygame.K_h:
                self._hiscores = HighScoresScreen()
                self._state    = GameState.HIGH_SCORES
            elif key == pygame.K_s:
                self._settings_screen = SettingsScreen(self._settings)
                self._state = GameState.SETTINGS

        elif self._state == GameState.PLAYING:
            if key == pygame.K_p:
                self._state = GameState.PAUSED

        elif self._state == GameState.PAUSED:
            if key in (pygame.K_p, pygame.K_SPACE):
                self._state = GameState.PLAYING

        elif self._state == GameState.GAME_OVER:
            if key == pygame.K_SPACE:
                self._begin_game()
            elif key == pygame.K_h:
                self._hiscores = HighScoresScreen()
                self._state    = GameState.HIGH_SCORES

        elif self._state == GameState.VICTORY:
            if key == pygame.K_SPACE:
                self._begin_game()

        elif self._state == GameState.LEVEL_COMPLETED:
            if self._lc and not self._lc.is_done():
                if key == pygame.K_SPACE:
                    self._lc.confirm()

        elif self._state == GameState.UPGRADE:
            if self._upgrade:
                self._upgrade.handle_key(key, self._session)

        elif self._state == GameState.SETTINGS:
            if self._settings_screen:
                self._settings_screen.handle_key(key)

        elif self._state == GameState.HIGH_SCORES:
            if self._hiscores:
                self._hiscores.handle_key(key)

        elif self._state == GameState.CREDITS:
            if self._credits:
                self._credits.handle_key(key)

    def _begin_game(self) -> None:
        self._session.full_reset()
        self._ready = ReadyScreen(self._session.level)
        self._state = GameState.READY

    def _update(self, snap) -> None:
        if self._state == GameState.SPLASH:
            if self._splash and not self._splash.update():
                self._splash = None
                self._state  = GameState.MENU

        elif self._state == GameState.READY:
            if self._ready and not self._ready.update():
                self._ready = None
                self._state = GameState.PLAYING

        elif self._state == GameState.PLAYING:
            next_state = self._session.update(snap)
            if next_state == GameState.LEVEL_COMPLETED:
                self._high_score = max(self._high_score, self._session.score)
                add_score(self._session.score, self._session.level)
                self._lc    = LevelCompletedScreen(
                    self._session.level,
                    self._session.score,
                    self._session.lives,
                )
                self._state = GameState.LEVEL_COMPLETED

            elif next_state == GameState.GAME_OVER:
                self._high_score = max(self._high_score, self._session.score)
                add_score(self._session.score, self._session.level)
                self._state = GameState.GAME_OVER

        elif self._state == GameState.LEVEL_COMPLETED:
            if self._lc and self._lc.is_done():
                self._session.score += self._lc.bonus
                if self._session.level >= TOTAL_LEVELS:
                    self._credits = CreditsScreen(self._session.score)
                    self._state   = GameState.CREDITS
                else:
                    self._upgrade = UpgradeScreen(self._session.score)
                    self._state   = GameState.UPGRADE

        elif self._state == GameState.UPGRADE:
            if self._upgrade and self._upgrade.done:
                self._upgrade = None
                self._session.start_next_level()
                self._ready = ReadyScreen(self._session.level)
                self._state = GameState.READY

        elif self._state == GameState.SETTINGS:
            if self._settings_screen and self._settings_screen.done:
                self._settings = self._settings_screen.config
                self._settings_screen = None
                self._state = GameState.MENU

        elif self._state == GameState.HIGH_SCORES:
            if self._hiscores and self._hiscores.done:
                self._hiscores = None
                self._state = GameState.MENU

        elif self._state == GameState.CREDITS:
            if self._credits:
                self._credits.update()
                if self._credits.done:
                    self._credits = None
                    self._state   = GameState.MENU

    def _render(self) -> None:
        self._screen.fill(Color.GRAY)

        if self._state == GameState.SPLASH and self._splash:
            self._splash.draw(self._screen)
            pygame.display.flip()
            return

        if self._state == GameState.SETTINGS and self._settings_screen:
            self._settings_screen.draw(self._screen)
            pygame.display.flip()
            return

        if self._state == GameState.HIGH_SCORES and self._hiscores:
            self._hiscores.draw(self._screen)
            pygame.display.flip()
            return

        if self._state == GameState.CREDITS and self._credits:
            self._credits.draw(self._screen)
            pygame.display.flip()
            return

        if self._state == GameState.UPGRADE and self._upgrade:
            self._upgrade.update_score(self._session.score)
            self._upgrade.draw(self._screen)
            pygame.display.flip()
            return

        pygame.draw.line(self._screen, (50, 50, 60), (0, 32), (SCREEN_WIDTH, 32))

        if self._state == GameState.MENU:
            self._hud.draw(self._screen, self._state,
                           self._session.score, self._session.lives,
                           self._high_score, self._session.level)

        elif self._state == GameState.READY and self._ready:
            self._session.draw(self._screen)
            self._ready.draw(self._screen, self._session.draw)
            self._hud.draw(self._screen, GameState.PLAYING,
                           self._session.score, self._session.lives,
                           self._high_score, self._session.level)

        elif self._state in (GameState.PLAYING, GameState.PAUSED):
            self._session.draw(self._screen)
            self._hud.draw(self._screen, self._state,
                           self._session.score, self._session.lives,
                           self._high_score, self._session.level)

        elif self._state == GameState.LEVEL_COMPLETED:
            self._session.draw(self._screen)
            self._hud.draw(self._screen, GameState.PLAYING,
                           self._session.score, self._session.lives,
                           self._high_score, self._session.level)
            if self._lc:
                self._lc.draw(self._screen)

        elif self._state in (GameState.GAME_OVER, GameState.VICTORY):
            self._session.draw(self._screen)
            self._hud.draw(self._screen, self._state,
                           self._session.score, self._session.lives,
                           self._high_score, self._session.level)

        pygame.display.flip()
