import pygame

pygame.display.init()
info = pygame.display.Info()

LARGURA_TOTAL = info.current_w
ALTURA = info.current_h

TITULO = "Tetris"

BOARD_ROWS = 22
BOARD_COLS = 10

TAMANHO_CELULA = min(int((ALTURA - 120) / BOARD_ROWS), 36)

LARGURA_REAL_TABULEIRO = BOARD_COLS * TAMANHO_CELULA
ALTURA_REAL_TABULEIRO  = BOARD_ROWS * TAMANHO_CELULA

BOARD_OFFSET_X = (LARGURA_TOTAL - LARGURA_REAL_TABULEIRO) // 2
BOARD_OFFSET_Y = (ALTURA - ALTURA_REAL_TABULEIRO) // 2

PANEL_W        = 180
PANEL_LEFT_X   = BOARD_OFFSET_X - PANEL_W - 20
PANEL_RIGHT_X  = BOARD_OFFSET_X + LARGURA_REAL_TABULEIRO + 20

FPS_BASE       = 60
BASE_FALL_TICKS = 48
FLASH_DURATION  = 12
LOCK_DELAY      = 20  

SCREEN_NAME       = "name_entry"
SCREEN_GAME       = "game"
SCREEN_GAME_OVER  = "game_over"
SCREEN_LEADERBOARD = "leaderboard"
SCREEN_CELEBRATION = "celebration"

C_BG          = (6,  11,  18)
C_BOARD_BG    = (4,   8,  14)
C_BORDER      = (0, 210, 130)
C_BORDER_DIM  = (8,  14,  20)
C_GHOST       = (80, 100, 140)
C_TEXT        = (180, 255, 210)
C_TEXT_DIM    = (70,  130, 100)
C_GOLD        = (255, 215,   0)
C_SILVER      = (192, 192, 192)
C_BRONZE      = (205, 127,  50)
C_ACCENT      = (0,  220, 140)
C_PANEL_BG    = (5,   9,  15)
C_DANGER      = (255,  50,  80)
C_LEVEL_UP    = (255, 230,   0)

PIECE_COLORS = {
    '⬜': (200, 240, 255),   # I
    '🟪': (150,  50, 255),   # O
    '🟨': (255, 220,   0),   # L
    '🟩': ( 50, 220,  80),   # J
    '🟦': (  0, 160, 255),   # S
    '🟥': (255,  50,  80),   # Z
    '🟧': (255, 140,   0),   # T
    '💣': (220,  50, 220),   # Bomba
}

SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}
LEVEL_LINES  = 10
MAX_SCORES   = 10
