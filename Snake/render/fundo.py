from __future__ import annotations
import pygame
import config.config as C


def grade_jogo(surf: pygame.Surface) -> None:
    """Grade fixa para a area de jogo."""
    surf.fill(C.COR_FUNDO)
    T = C.TAMANHO_CELULA
    for x in range(0, C.LARGURA_JOGO, T):
        pygame.draw.line(surf, C.COR_GRADE, (x, 0), (x, C.ALTURA))
    for y in range(0, C.ALTURA, T):
        pygame.draw.line(surf, C.COR_GRADE, (0, y), (C.LARGURA_JOGO, y))


def grade_simples(surf: pygame.Surface) -> None:
    """Grade para telas de menu sem animacao."""
    surf.fill(C.COR_FUNDO)
    T = C.TAMANHO_CELULA
    for x in range(0, C.LARGURA_TELA, T):
        cor = C.COR_GRADE_BRILHO if (x // T) % 5 == 0 else C.COR_GRADE
    for y in range(0, C.ALTURA, T):
        cor = C.COR_GRADE_BRILHO if (y // T) % 5 == 0 else C.COR_GRADE


def grade_brilhante(surf: pygame.Surface, frame: int) -> None:
    """Grade com linha de brilho que percorre a tela — usada em menus."""
    surf.fill(C.COR_FUNDO)
    T = C.TAMANHO_CELULA
    col_brilho = int(frame * 0.3) % (C.LARGURA_TELA // T)
    row_brilho = int(frame * 0.2) % (C.ALTURA // T)
    for xi, x in enumerate(range(0, C.LARGURA_TELA, T)):
        cor = C.COR_GRADE_BRILHO if xi == col_brilho else C.COR_GRADE
    for yi, y in enumerate(range(0, C.ALTURA, T)):
        cor = C.COR_GRADE_BRILHO if yi == row_brilho else C.COR_GRADE
