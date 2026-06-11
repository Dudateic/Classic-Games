import pygame
from core.board import Board
from core.scoring import Scorer
from engine.game_loop import GameEngine
from engine.input_handler import InputManager
from render.renderer import RenderPipeline
from config.settings import BOARD_ROWS, BOARD_COLS


class Application:
    def __init__(self):
        self.board   = Board(BOARD_ROWS, BOARD_COLS)
        self.scorer  = Scorer()
        self.input   = InputManager()
        self.renderer= RenderPipeline()
        self.engine  = GameEngine(self.board, self.scorer, self.input, self.renderer)

    def run(self):
        self.engine.start()
        pygame.quit()


if __name__ == "__main__":
    app = Application()
    app.run()
