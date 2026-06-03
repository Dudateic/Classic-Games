SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "Breakout"
TOTAL_LEVELS  = 5

class Color:
    BLACK      = (0,   0,   0)
    WHITE      = (255, 255, 255)
    GRAY       = (30,  30,  30)
    PADDLE     = (200, 200, 220)
    BALL       = (255, 220,  80)
    HUD_TEXT   = (180, 180, 200)
    GOLD       = (255, 215,   0)
    GREEN      = ( 60, 220,  80)
    RED        = (220,  60,  60)

    BRICK_ROWS = [
        (220,  60,  60),
        (220, 140,  40),
        (220, 220,  40),
        ( 60, 200,  80),
        ( 60, 140, 220),
        (160,  60, 220),
    ]

PADDLE_WIDTH  = 120
PADDLE_HEIGHT = 14
PADDLE_SPEED  = 7
PADDLE_Y      = SCREEN_HEIGHT - 60

BALL_RADIUS       = 8
BALL_SPEED_INIT   = 5.0
BALL_SPEED_MAX    = 12.0
BALL_SPEED_INC    = 0.15

BRICK_COLS        = 10
BRICK_ROWS        = 6
BRICK_WIDTH       = 64
BRICK_HEIGHT      = 22
BRICK_PADDING     = 6
BRICK_OFFSET_TOP  = 60
BRICK_OFFSET_LEFT = (SCREEN_WIDTH - BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING) // 2

BRICK_POINTS_BASE = 10

LIVES_START = 3

# Upgrades disponíveis na loja
UPGRADES = [
    {
        "id": "wide_paddle",
        "label": "Raquete Larga",
        "desc": "+40px na largura da raquete",
        "cost": 200,
        "icon": "▬",
    },
    {
        "id": "slow_ball",
        "label": "Bola Lenta",
        "desc": "Velocidade máx -20% neste nível",
        "cost": 150,
        "icon": "◉",
    },
    {
        "id": "extra_life",
        "label": "Vida Extra",
        "desc": "+1 vida (máx 5)",
        "cost": 300,
        "icon": "♥",
    },
    {
        "id": "score_boost",
        "label": "Boost de Pontos",
        "desc": "×2 pontos neste nível",
        "cost": 250,
        "icon": "★",
    },
]
