from __future__ import annotations
import pygame

_font_xs  = None
_font_sm  = None
_font_med = None
_font_lg  = None
_font_xl  = None
_font_xxl = None

def init() -> None:
    """Inicializa as fontes clássicas do sistema."""
    global _font_xs, _font_sm, _font_med, _font_lg, _font_xl, _font_xxl
    if _font_xs is None:
        _font_xs  = pygame.font.SysFont("monospace", 14, bold=True)
        _font_sm  = pygame.font.SysFont("monospace", 18, bold=True)
        _font_med = pygame.font.SysFont("monospace", 26, bold=True)
        _font_lg  = pygame.font.SysFont("monospace", 48, bold=True)
        _font_xl  = pygame.font.SysFont("monospace", 72, bold=True)
        _font_xxl = pygame.font.SysFont("monospace", 96, bold=True)


def get(tamanho: int) -> pygame.font.Font:
    """Retorna a fonte mais próxima do tamanho solicitado."""
    init()
    if tamanho <= 14: return _font_xs
    if tamanho <= 18: return _font_sm
    if tamanho <= 26: return _font_med
    if tamanho <= 48: return _font_lg
    if tamanho <= 72: return _font_xl
    return _font_xxl


def med() -> pygame.font.Font:
    """Retorna a fonte média de terminal para mensagens rápidas."""
    init()
    return _font_med