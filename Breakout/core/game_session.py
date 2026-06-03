import pygame
from core.config import LIVES_START, SCREEN_WIDTH, SCREEN_HEIGHT, Color, UPGRADES
from core.state import GameState
from core.input_handler import InputSnapshot
from entities.paddle import Paddle
from entities.ball import Ball
from entities.brick_grid import BrickGrid
from systems.particles import ParticleSystem


class GameSession:
    def __init__(self) -> None:
        self.paddle       = Paddle()
        self.ball         = Ball()
        self.brick_grid   = BrickGrid()
        self.particles    = ParticleSystem()
        self.score        = 0
        self.lives        = LIVES_START
        self.level        = 1
        self._active_upgrades: dict = {}
        self._score_multiplier: int = 1
        self._reset_round()

    def _reset_round(self) -> None:
        self.paddle.reset()
        self.ball.reset(self.paddle.rect)
        self.particles.clear()

    def full_reset(self) -> None:
        self.score  = 0
        self.lives  = LIVES_START
        self.level  = 1
        self._active_upgrades = {}
        self._score_multiplier = 1
        self.brick_grid.set_level(self.level)
        self._apply_paddle_upgrade()
        self._reset_round()

    def start_next_level(self) -> None:
        self.level += 1
        self._active_upgrades = {}
        self._score_multiplier = 1
        self.brick_grid.set_level(self.level)
        self._apply_paddle_upgrade()
        self._reset_round()

    def apply_upgrade(self, upgrade_id: str) -> bool:
        """Aplica upgrade; retorna False se custo > score."""
        upgrade = next((u for u in UPGRADES if u["id"] == upgrade_id), None)
        if not upgrade or self.score < upgrade["cost"]:
            return False
        self.score -= upgrade["cost"]
        self._active_upgrades[upgrade_id] = True

        if upgrade_id == "extra_life":
            self.lives = min(self.lives + 1, 5)
        elif upgrade_id == "score_boost":
            self._score_multiplier = 2
        elif upgrade_id == "slow_ball":
            from core.config import BALL_SPEED_MAX
            self.ball._speed = min(self.ball._speed, BALL_SPEED_MAX * 0.8)
        elif upgrade_id == "wide_paddle":
            self._apply_paddle_upgrade()
        return True

    def _apply_paddle_upgrade(self) -> None:
        from core.config import PADDLE_WIDTH
        extra = 40 if self._active_upgrades.get("wide_paddle") else 0
        self.paddle.rect.width = PADDLE_WIDTH + extra

    def update(self, snap: InputSnapshot) -> GameState:
        dt = 1 / 60

        if pygame.K_SPACE in snap.keys_pressed:
            self.ball.launch()

        self.paddle.update(snap)
        ball_alive = self.ball.update(self.paddle.rect)

        points, reflect_v, reflect_h, hit_color = self.brick_grid.collide_ball(self.ball.rect)

        if reflect_v:
            self.ball.reflect_vertical()
        if reflect_h:
            self.ball.reflect_horizontal()
        if points:
            self.score += points * self._score_multiplier
            self.ball.increase_speed()
            if hit_color:
                cx, cy = self.ball.rect.center
                self.particles.emit(cx, cy, hit_color, count=14)

        self.particles.update(dt)

        if self.brick_grid.all_destroyed:
            return GameState.LEVEL_COMPLETED

        if not ball_alive:
            self.lives -= 1
            if self.lives <= 0:
                return GameState.GAME_OVER
            self._reset_round()

        return GameState.PLAYING

    def draw(self, surface: pygame.Surface) -> None:
        self.brick_grid.draw(surface)
        self.particles.draw(surface)
        self.paddle.draw(surface)
        self.ball.draw(surface)
