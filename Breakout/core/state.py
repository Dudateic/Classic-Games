from enum import Enum, auto


class GameState(Enum):
    SPLASH          = auto()   # tela do estúdio/dev
    MENU            = auto()   # menu principal
    SETTINGS        = auto()   # configurações
    READY           = auto()   # contagem 3-2-1
    PLAYING         = auto()   # jogando
    PAUSED          = auto()   # pausado
    LEVEL_COMPLETED = auto()   # entre níveis
    UPGRADE         = auto()   # loja de melhorias
    GAME_OVER       = auto()   # perdeu
    VICTORY         = auto()   # venceu todos os níveis
    CREDITS         = auto()   # créditos finais
    HIGH_SCORES     = auto()   # ranking top 5
