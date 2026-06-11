import pygame, math, random
from config.settings import (
    TAMANHO_CELULA, BOARD_OFFSET_X, BOARD_OFFSET_Y,
    LARGURA_REAL_TABULEIRO, ALTURA_REAL_TABULEIRO,
    C_BG, C_BOARD_BG, C_BORDER, C_BORDER_DIM, PIECE_COLORS,
    LARGURA_TOTAL, ALTURA, C_GHOST, C_TEXT, C_TEXT_DIM, C_PANEL_BG,
    C_GOLD, C_SILVER, C_BRONZE, C_ACCENT, C_DANGER, C_LEVEL_UP,
    PANEL_LEFT_X, PANEL_RIGHT_X, PANEL_W,
    SCREEN_NAME, SCREEN_GAME, SCREEN_GAME_OVER,
    SCREEN_LEADERBOARD, SCREEN_CELEBRATION,
)
from core.pieces import PieceFactory, EMPTY
from render.effects import EffectManager

def _font(size, bold=False):
    for name in (       
        'JetBrains Mono',
        'Fira Code',
        'Cascadia Mono',
        'Consolas',
        'IBM Plex Mono',
        'DejaVu Sans Mono',
        ):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)

def _font_display(size, bold=True):
    for name in (
        'Orbitron',
        'Eurostile',
        'Bahnschrift',
        'Montserrat',
        'Poppins',
        'Segoe UI',
    ):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)


class RenderPipeline:
    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((LARGURA_TOTAL, ALTURA))
        pygame.display.set_caption("Tetris")
        self.effects = EffectManager()

        self.f_tiny    = _font(17)
        self.f_small   = _font(18)
        self.f_med     = _font(22, bold=True)
        self.f_large   = _font_display(40)
        self.f_huge    = _font_display(72)
        self.f_title   = _font_display(96, bold=True)

        self._tick       = 0
        self._bg_stars   = [(random.randint(0, LARGURA_TOTAL),
                             random.randint(0, ALTURA),
                             random.uniform(0.3, 1.5))
                            for _ in range(120)]


    def _draw_cell(self, x: int, y: int, color: tuple, is_ghost=False, alpha=255) -> None:
        sz   = TAMANHO_CELULA
        rect = pygame.Rect(x+1, y+1, sz-2, sz-2)

        if is_ghost:
            s = pygame.Surface((sz-2, sz-2), pygame.SRCALPHA)
            pygame.draw.rect(s, (*C_GHOST, 60), (0,0,sz-2,sz-2), border_radius=3)
            pygame.draw.rect(s, (*C_GHOST, 120), (0,0,sz-2,sz-2), width=1, border_radius=3)
            self.screen.blit(s, (x+1, y+1))
            return

        r, g, b = color
        if alpha < 255:
            s = pygame.Surface((sz-2, sz-2), pygame.SRCALPHA)
            pygame.draw.rect(s, (r,g,b, alpha), (0,0,sz-2,sz-2), border_radius=3)
            self.screen.blit(s, (x+1, y+1))
            return

        pygame.draw.rect(self.screen, color, rect, border_radius=3)
        light = (min(255, r+60), min(255, g+60), min(255, b+60))
        dark  = (max(0, r-60), max(0, g-60), max(0, b-60))
        pygame.draw.line(self.screen, light, (x+2, y+2), (x+sz-3, y+2), 1)
        pygame.draw.line(self.screen, light, (x+2, y+2), (x+2, y+sz-3), 1)
        pygame.draw.line(self.screen, dark,  (x+2, y+sz-3), (x+sz-3, y+sz-3), 1)
        pygame.draw.line(self.screen, dark,  (x+sz-3, y+2), (x+sz-3, y+sz-3), 1)

    def _text(self, surf, text, x, y, color, font=None, center=False, shadow=True):
        f = font or self.f_small
        if shadow:
            s = f.render(text, True, (0,0,0))
            sr = s.get_rect()
            if center:
                sr.centerx = x
                sr.top = y
            else:
                sr.topleft = (x, y)
            surf.blit(s, (sr.x+2, sr.y+2))
        ts = f.render(text, True, color)
        tr = ts.get_rect()
        if center:
            tr.centerx = x
            tr.top = y
        else:
            tr.topleft = (x, y)
        surf.blit(ts, tr)

    def _draw_panel(self, x, y, w, h, title=''):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*C_PANEL_BG, 200))
        pygame.draw.rect(s, (*C_BORDER, 80), (0,0,w,h), width=1, border_radius=4)
        self.screen.blit(s, (x, y))
        if title:
            self._text(self.screen, title, x + w//2, y + 8, C_TEXT_DIM,
                       font=self.f_tiny, center=True, shadow=False)

    def _draw_mini_piece(self, piece, cx, cy, cell_size=16):
        if piece is None:
            return
        m   = piece.matrix
        rows, cols = len(m), len(m[0])
        ox  = cx - (cols * cell_size) // 2
        oy  = cy - (rows * cell_size) // 2
        for r, row in enumerate(m):
            for c, cell in enumerate(row):
                if cell != EMPTY:
                    color = PIECE_COLORS.get(cell, (200,200,200))
                    x = ox + c * cell_size
                    y = oy + r * cell_size
                    rect = pygame.Rect(x+1, y+1, cell_size-2, cell_size-2)
                    pygame.draw.rect(self.screen, color, rect, border_radius=2)

    def _draw_stars(self):
        for sx, sy, brightness in self._bg_stars:
            b = int(brightness * 80 + 20 * math.sin(self._tick * 0.04 + sx))
            b = max(10, min(180, b))
            pygame.draw.circle(self.screen, (b,b,b), (int(sx), int(sy)), 1)


    def draw_name_entry(self, name: str, blink: bool):
        self.screen.fill(C_BG)
        self._draw_stars()

        cx = LARGURA_TOTAL // 2

        pulse = int(30 * math.sin(self._tick * 0.05))
        color = (0, min(255, 200+pulse), min(255, 130+pulse))
        self._text(self.screen, 'TETRIS', cx, 80, color, font=self.f_title, center=True)
        box_w, box_h = 420, 70
        bx = cx - box_w//2
        by = ALTURA//2 - 80

        self._text(self.screen, 'SEU NOME', cx, by - 50, C_TEXT_DIM,
                   font=self.f_med, center=True, shadow=False)

        bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg.fill((*C_PANEL_BG, 220))
        border_c = C_ACCENT if blink else C_BORDER
        pygame.draw.rect(bg, (*border_c, 200), (0,0,box_w,box_h), width=2, border_radius=8)
        self.screen.blit(bg, (bx, by))

        cursor = '|' if blink else ''
        display = name + cursor
        self._text(self.screen, display, cx, by + 18, C_GOLD,
                   font=self.f_large, center=True)

        self._text(self.screen, 'ENTER  para começar', cx, by + 120,
                   C_TEXT_DIM, font=self.f_small, center=True, shadow=False)

        pygame.display.flip()


    def draw_board(self, board, flashing_lines: dict, shake=(0,0)) -> None:
        ox = BOARD_OFFSET_X + shake[0]
        oy = BOARD_OFFSET_Y + shake[1]

        board_rect = pygame.Rect(ox, oy, LARGURA_REAL_TABULEIRO, ALTURA_REAL_TABULEIRO)
        pygame.draw.rect(self.screen, C_BOARD_BG, board_rect)

        for r in range(board.rows + 1):
            y = oy + r * TAMANHO_CELULA
            pygame.draw.line(self.screen, (12,20,30),
                             (ox, y), (ox + LARGURA_REAL_TABULEIRO, y), 1)
        for c in range(board.cols + 1):
            x = ox + c * TAMANHO_CELULA
            pygame.draw.line(self.screen, (12,20,30),
                             (x, oy), (x, oy + ALTURA_REAL_TABULEIRO), 1)

        # Blocos
        for r, row in enumerate(board.grid):
            for c, cell in enumerate(row):
                if cell != board.empty:
                    color = PIECE_COLORS.get(cell, (200,200,200))
                    if r in flashing_lines:
                        t     = flashing_lines[r]
                        alpha = int(255 * abs(math.sin(t * 0.5)))
                        self._draw_cell(ox + c*TAMANHO_CELULA, oy + r*TAMANHO_CELULA,
                                        (255,255,255), alpha=alpha)
                    else:
                        self._draw_cell(ox + c*TAMANHO_CELULA, oy + r*TAMANHO_CELULA, color)

        glow = int(40 * math.sin(self._tick * 0.04))
        bc   = (0, min(255, 200+glow), min(255, 120+glow))
        pygame.draw.rect(self.screen, bc, board_rect, width=2, border_radius=2)

    def draw_piece(self, piece, row, col, ghost_row, shake=(0,0)) -> None:
        ox = BOARD_OFFSET_X + shake[0]
        oy = BOARD_OFFSET_Y + shake[1]

        for r, c, cell in PieceFactory.yield_cells(piece.matrix, ghost_row, col):
            self._draw_cell(ox + c*TAMANHO_CELULA, oy + r*TAMANHO_CELULA,
                            PIECE_COLORS.get(cell,(255,255,255)), is_ghost=True)

        for r, c, cell in PieceFactory.yield_cells(piece.matrix, row, col):
            self._draw_cell(ox + c*TAMANHO_CELULA, oy + r*TAMANHO_CELULA,
                            PIECE_COLORS.get(cell,(255,255,255)))


    def draw_left_panel(self, hold_piece, score, lines, level, player_name):
        x  = PANEL_LEFT_X
        pw = PANEL_W

        if hold_piece:
            self._draw_mini_piece(hold_piece, x + pw//2, BOARD_OFFSET_Y + 58)

        sy = BOARD_OFFSET_Y
        stats = [('JOGADOR', player_name, C_GOLD),
                 ('SCORE',   f'{int(score):,}', C_ACCENT),
                 ('LINHAS',  str(lines), C_TEXT),
                 ('NÍVEL',   str(level), C_LEVEL_UP)]

        for label, val, vc in stats:
            self._draw_panel(x, sy, pw, 68)
            self._text(self.screen, label, x + pw//2, sy + 8, C_TEXT_DIM,
                       font=self.f_tiny, center=True, shadow=False)
            self._text(self.screen, val, x + pw//2, sy + 28, vc,
                       font=self.f_med, center=True)
            sy += 76


    def draw_right_panel(self, next_pieces: list):
        x  = PANEL_RIGHT_X
        pw = PANEL_W
        self._draw_panel(x, BOARD_OFFSET_Y, pw, 30 + len(next_pieces)*80, 'PRÓXIMA')
        for i, piece in enumerate(next_pieces):
            py = BOARD_OFFSET_Y + 40 + i * 80
            self._draw_mini_piece(piece, x + pw//2, py + 28, cell_size=18)
            if i < len(next_pieces)-1:
                pygame.draw.line(self.screen, C_BORDER_DIM,
                                 (x+10, py+66), (x+pw-10, py+66), 1)


    def render_frame(self, board, current_piece, piece_row, piece_col,
                     ghost_row, score, lines, level, player_name,
                     hold_piece, next_pieces, is_paused=False, is_game_over=False):
        self._tick += 1
        self.screen.fill(C_BG)
        self._draw_stars()

        shake = self.effects.shake_offset

        self.draw_board(board, self.effects.flashing_lines, shake)
        if current_piece:
            self.draw_piece(current_piece, piece_row, piece_col, ghost_row, shake)

        self.draw_left_panel(hold_piece, score, lines, level, player_name)
        self.draw_right_panel(next_pieces)

        self.effects.update()
        self.effects.draw(self.screen)

        if is_paused:
            self._draw_overlay('PAUSADO', C_TEXT, subtitle='P  para continuar')

        pygame.display.flip()


    def render_game_over(self, score, lines, level, player_name, rank):
        self._tick += 1
        self.screen.fill(C_BG)
        self._draw_stars()
        self.effects.update()
        self.effects.draw(self.screen)

        cx = LARGURA_TOTAL // 2
        cy = ALTURA // 2

        ov = pygame.Surface((LARGURA_TOTAL, ALTURA), pygame.SRCALPHA)
        ov.fill((0, 0, 5, 200))
        self.screen.blit(ov, (0,0))

        pulse = int(20 * abs(math.sin(self._tick * 0.06)))
        r = min(255, 200+pulse)
        self._text(self.screen, 'GAME OVER', cx, cy - 200, (r, 40, 60),
                   font=self.f_title, center=True)

        box_w, box_h = 500, 200
        bx, by = cx - box_w//2, cy - 80
        bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg.fill((5, 12, 20, 220))
        pygame.draw.rect(bg, (*C_BORDER, 100), (0,0,box_w,box_h), width=1, border_radius=8)
        self.screen.blit(bg, (bx, by))

        self._text(self.screen, player_name, cx, by+16, C_GOLD,
                   font=self.f_large, center=True)

        row_data = [
            ('PONTUAÇÃO', f'{int(score):,}', C_ACCENT),
            ('LINHAS',    str(lines),         C_TEXT),
            ('NÍVEL',     str(level),          C_LEVEL_UP),
        ]
        for i, (lbl, val, vc) in enumerate(row_data):
            rx = bx + 30 + i * 155
            self._text(self.screen, lbl, rx+65, by+70, C_TEXT_DIM,
                       font=self.f_tiny, center=True, shadow=False)
            self._text(self.screen, val, rx+65, by+90, vc,
                       font=self.f_med, center=True)

        rank_colors = {1: C_GOLD, 2: C_SILVER, 3: C_BRONZE}
        rc = rank_colors.get(rank, C_TEXT)
        self._text(self.screen, f'#{rank}º LUGAR', cx, by+150, rc,
                   font=self.f_large, center=True)

        self._text(self.screen, 'ENTER  jogar novamente     P  ver placar',
                   cx, cy + 150, C_TEXT_DIM, font=self.f_small, center=True, shadow=False)

        pygame.display.flip()


    def render_leaderboard(self, scores: list, highlight_name='', highlight_score=0):
        self._tick += 1
        self.screen.fill(C_BG)
        self._draw_stars()
        self.effects.update()
        self.effects.draw(self.screen)

        cx = LARGURA_TOTAL // 2

        pulse = int(25 * math.sin(self._tick * 0.05))
        self._text(self.screen, 'PLACAR', cx, 60, C_GOLD, font=self.f_title, center=True)

        tw, th = 640, 52
        tx = cx - tw//2
        ty = 180

        headers = ['#', 'NOME', 'SCORE', 'LINHAS', 'NÍV']
        hx      = [tx+16, tx+80, tx+300, tx+460, tx+570]
        for i, h in enumerate(headers):
            self._text(self.screen, h, hx[i], ty, C_TEXT_DIM,
                       font=self.f_tiny, shadow=False)

        pygame.draw.line(self.screen, C_BORDER_DIM, (tx, ty+18), (tx+tw, ty+18), 1)

        rank_colors = {0: C_GOLD, 1: C_SILVER, 2: C_BRONZE}

        for i, entry in enumerate(scores[:10]):
            ry = ty + 28 + i * 44
            is_me = (entry['name'] == highlight_name.upper()[:12] and
                     entry['score'] == highlight_score)

            if is_me:
                hs = pygame.Surface((tw, 40), pygame.SRCALPHA)
                hs.fill((0, 200, 120, 40))
                self.screen.blit(hs, (tx, ry-4))
                pygame.draw.rect(self.screen, (*C_ACCENT, 150),
                                 (tx, ry-4, tw, 40), width=1, border_radius=3)

            rc  = rank_colors.get(i, C_TEXT)
            num = ['🥇','🥈','🥉'][i] if i < 3 else str(i+1)

            medal_txt = ['1st','2nd','3rd'][i] if i < 3 else f'{i+1}.'
            self._text(self.screen, medal_txt, hx[0], ry, rc, font=self.f_tiny, shadow=False)
            self._text(self.screen, entry['name'], hx[1], ry, rc if is_me else C_TEXT,
                       font=self.f_small)
            self._text(self.screen, f"{entry['score']:,}", hx[2], ry,
                       C_ACCENT if is_me else C_TEXT, font=self.f_small)
            self._text(self.screen, str(entry['lines']), hx[3], ry, C_TEXT,
                       font=self.f_small)
            self._text(self.screen, str(entry['level']), hx[4], ry, C_LEVEL_UP,
                       font=self.f_small)

            pygame.draw.line(self.screen, (15,25,35),
                             (tx, ry+36), (tx+tw, ry+36), 1)

        pygame.display.flip()


    def render_celebration(self, player_name: str, score: int):
        self._tick += 1
        self.screen.fill(C_BG)
        self._draw_stars()

        if self._tick % 4 == 0:
            self.effects.spawn_celebration(LARGURA_TOTAL, ALTURA)

        self.effects.update()
        self.effects.draw(self.screen)

        cx = LARGURA_TOTAL // 2
        cy = ALTURA // 2

        pulse = abs(math.sin(self._tick * 0.07))
        for i in range(5):
            r = 300 - i*40
            a = int(30 * pulse * (1 - i/5))
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*C_GOLD, a), (r, r), r)
            self.screen.blit(s, (cx-r, cy-r-80))

        self._text(self.screen, 'NOVO RECORDE!', cx, cy - 230,
                   C_GOLD, font=self.f_title, center=True)

        self._text(self.screen, player_name, cx, cy - 110,
                   (255, 255, 255), font=self.f_huge, center=True)

        self._text(self.screen, f'{int(score):,} PONTOS', cx, cy - 20,
                   C_ACCENT, font=self.f_large, center=True)

        self._text(self.screen, 'VOCÊ É O NOVO #1', cx, cy + 60,
                   C_GOLD, font=self.f_med, center=True)

        blink = (self._tick // 25) % 2 == 0
        if blink:
            self._text(self.screen, 'ENTER  para ver o placar', cx, cy + 140,
                       C_TEXT_DIM, font=self.f_small, center=True, shadow=False)

        pygame.display.flip()


    def _draw_overlay(self, title, color, subtitle=''):
        ov = pygame.Surface((LARGURA_TOTAL, ALTURA), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        self.screen.blit(ov, (0,0))
        cx = LARGURA_TOTAL//2
        cy = ALTURA//2
        self._text(self.screen, title, cx, cy-40, color, font=self.f_huge, center=True)
        if subtitle:
            self._text(self.screen, subtitle, cx, cy+40, C_TEXT_DIM,
                       font=self.f_small, center=True, shadow=False)
