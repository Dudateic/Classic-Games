import pygame
from core.config import LIVES_START, SCREEN_WIDTH, SCREEN_HEIGHT, Color
from core.state import GameState
from core.input_handler import InputSnapshot
from entities.paddle import Paddle
from entities.ball import Ball
from entities.brick_grid import BrickGrid

class GameSession:
    def __init__(self) -> None:
        self.paddle     = Paddle()
        self.ball       = Ball()
        self.brick_grid = BrickGrid()
        self.score      = 0
        self.lives      = LIVES_START
        self._reset_round()

    def _reset_round(self) -> None:
        self.paddle.reset()
        self.ball.reset(self.paddle.rect)

    def full_reset(self) -> None:
        self.score = 0
        self.lives = LIVES_START
        self.brick_grid.reset()
        self._reset_round()

    def update(self, snap: InputSnapshot) -> GameState:

        if pygame.K_SPACE in snap.keys_pressed:
            self.ball.launch()

        self.paddle.update(snap)

        ball_alive = self.ball.update(self.paddle.rect)

        points, reflect_v, reflect_h = self.brick_grid.collide_ball(self.ball.rect)
        if reflect_v:
            self.ball.reflect_vertical()
        if reflect_h:
            self.ball.reflect_horizontal()
        if points:
            self.score += points
            self.ball.increase_speed()

        if self.brick_grid.all_destroyed:
            return GameState.VICTORY

        if not ball_alive:
            self.lives -= 1
            if self.lives <= 0:
                return GameState.GAME_OVER
            self._reset_round()

        return GameState.PLAYING

    def draw(self, surface: pygame.Surface) -> None:
        self.brick_grid.draw(surface)
        self.paddle.draw(surface)
        self.ball.draw(surface)
