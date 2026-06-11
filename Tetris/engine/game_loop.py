import pygame
from collections import deque

from core.board import Board
from core.pieces import PieceFactory, Piece
from core.scoring import Scorer, save_score, get_first_place_score, load_scores
from config.settings import (
    BOARD_ROWS, BOARD_COLS, FPS_BASE, TAMANHO_CELULA,
    BOARD_OFFSET_X, BOARD_OFFSET_Y,
    SCREEN_NAME, SCREEN_GAME, SCREEN_GAME_OVER,
    SCREEN_LEADERBOARD, SCREEN_CELEBRATION,
    LOCK_DELAY,
)

NEXT_COUNT = 3


class GameEngine:

    def __init__(self, board: Board, scorer: Scorer, input_manager, renderer):
        self.board    = board
        self.scorer   = scorer
        self.input    = input_manager
        self.renderer = renderer

        self.is_running  = True
        self.screen      = SCREEN_NAME

        self.current_piece  = None
        self.piece_row      = 0
        self.piece_col      = 0
        self.fall_counter   = 0
        self.lock_counter   = 0
        self.is_landing     = False
        self.is_paused      = False

        self.hold_piece     = None
        self.hold_used      = False

        self.next_queue: deque[Piece] = deque()
        for _ in range(NEXT_COUNT + 1):
            self.next_queue.append(PieceFactory.create_random())

        self.player_name = ''
        self._cursor_blink = 0

        self.final_rank  = 0
        self.scores_list = []
        self._prev_first_score = get_first_place_score()
        self._celebration_timer = 180


    def start(self):
        clock = pygame.time.Clock()
        while self.is_running:
            self.input.poll_events()
            if self.input.quit_requested:
                self.is_running = False
                break

            if self.screen == SCREEN_NAME:
                self._update_name_entry()
                self.renderer.draw_name_entry(self.player_name, self._cursor_blink > 15)
            elif self.screen == SCREEN_GAME:
                self._update_game()
                self.renderer.render_frame(
                    self.board, self.current_piece,
                    self.piece_row, self.piece_col,
                    self._ghost_row(),
                    self.scorer.score, self.scorer.lines, self.scorer.level,
                    self.player_name,
                    self.hold_piece, list(self.next_queue)[:NEXT_COUNT],
                    is_paused=self.is_paused,
                )
            elif self.screen == SCREEN_GAME_OVER:
                self._update_game_over_screen()
                self.renderer.render_game_over(
                    self.scorer.score, self.scorer.lines, self.scorer.level,
                    self.player_name, self.final_rank,
                )
            elif self.screen == SCREEN_LEADERBOARD:
                self._update_leaderboard_screen()
                self.renderer.render_leaderboard(
                    self.scores_list, self.player_name, int(self.scorer.score),
                )
            elif self.screen == SCREEN_CELEBRATION:
                self._update_celebration_screen()
                self.renderer.render_celebration(self.player_name, self.scorer.score)

            clock.tick(FPS_BASE)

    def _update_name_entry(self):
        self._cursor_blink = (self._cursor_blink + 1) % 30
        if self.input.text_input and len(self.player_name) < 12:
            self.player_name += self.input.text_input
        if self.input.backspace and self.player_name:
            self.player_name = self.player_name[:-1]
        if self.input.confirm and self.player_name.strip():
            self._start_game()

    def _start_game(self):
        self.board.reset()
        self.scorer.score = 0.0
        self.scorer.lines = 0
        self.scorer.level = 1
        self.scorer.combo = 0
        self.fall_counter = 0
        self.hold_piece   = None
        self.hold_used    = False
        self.is_paused    = False
        self.next_queue   = deque(PieceFactory.create_random() for _ in range(NEXT_COUNT+1))
        self._prev_first_score = get_first_place_score()
        self._spawn_piece()
        self.screen = SCREEN_GAME

    def _spawn_piece(self):
        self.current_piece = self.next_queue.popleft()
        self.next_queue.append(PieceFactory.create_random())
        self.piece_row  = 0
        self.piece_col  = (self.board.cols - self.current_piece.cols) // 2
        self.fall_counter = 0
        self.lock_counter = 0
        self.is_landing   = False
        self.hold_used    = False

        if self.board.has_collision(self.current_piece.matrix, self.piece_row, self.piece_col):
            self._trigger_game_over()

    def _update_game(self):
        if self.is_paused:
            if self.input.pause_requested:
                self.is_paused = False
            return

        if self.input.pause_requested:
            self.is_paused = True
            return

        self._process_movement()
        self._update_physics()

    def _process_movement(self):
        if self.input.move_x:
            self._try_move(self.input.move_x)

        if self.input.rotate_cw:
            rm = self.current_piece.get_rotated_matrix()
            if not self.board.has_collision(rm, self.piece_row, self.piece_col):
                self.current_piece.rotate_cw()
                if self.is_landing:
                    self.lock_counter = 0

        if self.input.rotate_ccw:
            self.current_piece.rotate_ccw()
            if self.board.has_collision(self.current_piece.matrix, self.piece_row, self.piece_col):
                self.current_piece.rotate_cw()   # desfaz
            elif self.is_landing:
                self.lock_counter = 0

        if self.input.hold:
            self._do_hold()

    def _update_physics(self):
        self.fall_counter += 1

        gravity_ticks = 2 if self.input.fast_drop else self.scorer.get_current_fall_ticks()

        if self.fall_counter >= gravity_ticks:
            self.fall_counter = 0

            can_fall = not self.board.has_collision(
                self.current_piece.matrix,
                self.piece_row + 1,
                self.piece_col
            )

            if can_fall:
                self.piece_row += 1

        touching_ground = self.board.has_collision(
            self.current_piece.matrix,
            self.piece_row + 1,
            self.piece_col
        )

        if touching_ground:
            self.is_landing = True
            self.lock_counter += 1

            if self.lock_counter >= LOCK_DELAY:
                self._lock_piece()
        else:
            self.is_landing = False
            self.lock_counter = 0

    def _lock_piece(self):
        color = self.current_piece.get_color()
        cx = BOARD_OFFSET_X + self.piece_col * TAMANHO_CELULA
        cy = BOARD_OFFSET_Y + self.piece_row * TAMANHO_CELULA

        if self.current_piece.is_bomb:
            self.renderer.effects.spawn_bomb(cx + TAMANHO_CELULA//2, cy + TAMANHO_CELULA//2)
            self.board.explode(self.piece_row, self.piece_col)
        else:
            self.renderer.effects.spawn_piece_lock(cx + TAMANHO_CELULA//2,
                                                   cy + TAMANHO_CELULA//2, color)
            self.board.stamp_piece(self.current_piece.matrix, self.piece_row, self.piece_col)

        lines_cleared, cleared_rows = self.board.clear_full_lines()
        pts = self.scorer.add_lines(lines_cleared)

        if lines_cleared > 0:
            self.renderer.effects.spawn_line_clear(
                cleared_rows, self.board, TAMANHO_CELULA, BOARD_OFFSET_X, BOARD_OFFSET_Y)
            self.renderer.effects.spawn_score_popup(pts,
                BOARD_OFFSET_X + LARGURA_REAL_TABULEIRO_HALF(),
                BOARD_OFFSET_Y + self.piece_row * TAMANHO_CELULA)
            self.renderer.effects.spawn_combo(self.scorer.combo,
                BOARD_OFFSET_X + LARGURA_REAL_TABULEIRO_HALF(),
                BOARD_OFFSET_Y + self.piece_row * TAMANHO_CELULA - 30)
            if lines_cleared == 4:
                self.renderer.effects.spawn_tetris(
                    self.board, TAMANHO_CELULA, BOARD_OFFSET_X, BOARD_OFFSET_Y,
                    BOARD_OFFSET_X + LARGURA_REAL_TABULEIRO_HALF(),
                    BOARD_OFFSET_Y + self.piece_row * TAMANHO_CELULA)

            old_level = (self.scorer.lines - lines_cleared) // 10 + 1
            if self.scorer.level > old_level:
                self.renderer.effects.spawn_level_up(
                    self.scorer.level,
                    BOARD_OFFSET_X + LARGURA_REAL_TABULEIRO_HALF(),
                    BOARD_OFFSET_Y + BOARD_ROWS * TAMANHO_CELULA // 2)

        self._spawn_piece()

    def _try_move(self, dx: int):
        nc = self.piece_col + dx
        if not self.board.has_collision(self.current_piece.matrix, self.piece_row, nc):
            self.piece_col = nc
            if self.is_landing:
                self.lock_counter = 0

    def _do_hold(self):
        if self.hold_used:
            return
        if self.hold_piece is None:
            self.hold_piece = self.current_piece
            self._spawn_piece()
        else:
            self.hold_piece, self.current_piece = self.current_piece, self.hold_piece
            self.piece_row  = 0
            self.piece_col  = (self.board.cols - self.current_piece.cols) // 2
            self.fall_counter = 0
            self.lock_counter = 0
            self.is_landing   = False
        self.hold_used = True

    def _do_hard_drop(self):
        ghost = self._ghost_row()
        drop_dist = ghost - self.piece_row
        self.scorer.score += drop_dist * 2
        self.piece_row = ghost
        self._lock_piece()

    def _ghost_row(self) -> int:
        if self.current_piece is None:
            return 0
        gr = self.piece_row
        while not self.board.has_collision(self.current_piece.matrix, gr+1, self.piece_col):
            gr += 1
        return gr

    def _trigger_game_over(self):
        prev_first = self._prev_first_score
        self.scores_list, self.final_rank = save_score(
            self.player_name, int(self.scorer.score),
            self.scorer.lines, self.scorer.level)

        beat_first = (int(self.scorer.score) > prev_first and self.final_rank == 1
                      and len(self.scores_list) > 1)

        if beat_first:
            self.renderer.effects.spawn_celebration(
                self.renderer.screen.get_width(), self.renderer.screen.get_height())
            self._celebration_timer = 300
            self.screen = SCREEN_CELEBRATION
        else:
            self.screen = SCREEN_GAME_OVER

    def _update_game_over_screen(self):
        if self.input.restart_requested:
            self._start_game()
        elif self.input.pause_requested:
            self.screen = SCREEN_LEADERBOARD

    def _update_leaderboard_screen(self):
        if self.input.restart_requested or self.input.confirm:
            self.screen = SCREEN_NAME

    def _update_celebration_screen(self):
        self._celebration_timer -= 1
        if self._celebration_timer <= 0 or self.input.confirm:
            self.screen = SCREEN_LEADERBOARD


def LARGURA_REAL_TABULEIRO_HALF():
    from config.settings import LARGURA_REAL_TABULEIRO
    return LARGURA_REAL_TABULEIRO // 2
