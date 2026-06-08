from __future__ import annotations
import pygame
import config.config as C
from entities.entities import Cobra, Fruta, Particula
from render.fundo import grade_jogo


def desenhar_tudo(surf: pygame.Surface, estado, frame: int) -> None:
    """Renderiza um frame completo da area de jogo (sem HUD)."""
    grade_jogo(surf)
    particulas(surf, estado.particulas)
    frutas(surf, estado.frutas)
    cobra(surf, estado.cobra, estado.boost_ativo, frame)


def cobra(surf: pygame.Surface, c: Cobra, boost: bool, frame: int) -> None:
    T = C.TAMANHO_CELULA
    n = len(c.corpo)
    for i, (x, y) in enumerate(c.corpo):
        t_norm   = i / max(n - 1, 1)
        cor_base = _cor_segmento(i, t_norm, boost, frame)
        rect     = pygame.Rect(x + 1, y + 1, T - 2, T - 2)
        pygame.draw.rect(surf, cor_base, rect, border_radius=3)
        pygame.draw.rect(surf, C.COBRA_BORDA, rect, width=1, border_radius=3)
        if i == 0:
            _olhos(surf, x, y, c.direcao)


def frutas(surf: pygame.Surface, lista: list[Fruta]) -> None:
    T = C.TAMANHO_CELULA
    for fruta in lista:
        x, y = fruta.pos
        rect  = pygame.Rect(x + 2, y + 2, T - 4, T - 4)
        pygame.draw.rect(surf, fruta.cor, rect, border_radius=4)
        brilho = tuple(min(255, int(c * 1.5)) for c in fruta.cor)
        pygame.draw.circle(surf, brilho, (x + 5, y + 5), 2)
        pygame.draw.rect(surf, C.PRETO, rect, width=1, border_radius=4)


def particulas(surf: pygame.Surface, lista: list[Particula]) -> None:
    for p in lista:
        r = int(p.raio)
        if r < 1:
            continue
        halo = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(halo, (*p.cor, p.alpha), (r + 1, r + 1), r)
        surf.blit(halo, (int(p.x) - r - 1, int(p.y) - r - 1))


def _cor_segmento(i: int, t_norm: float, boost: bool, frame: int) -> tuple:
    if boost:
        return C.ARCO_IRIS_NEON[(frame // 2 + i) % len(C.ARCO_IRIS_NEON)]
    r = int(C.COBRA_CABECA[0] * (1 - t_norm) + C.COBRA_CORPO_2[0] * t_norm)
    g = int(C.COBRA_CABECA[1] * (1 - t_norm) + C.COBRA_CORPO_2[1] * t_norm)
    b = int(C.COBRA_CABECA[2] * (1 - t_norm) + C.COBRA_CORPO_2[2] * t_norm)
    return (r, g, b)


def _olhos(surf: pygame.Surface, x: int, y: int, direcao: str) -> None:
    T = C.TAMANHO_CELULA
    r_olho, r_pupila = T // 5, T // 8
    if direcao == "DIREITA":    pts = [(x + T - 4, y + 4),    (x + T - 4, y + T - 4)]
    elif direcao == "ESQUERDA": pts = [(x + 4,     y + 4),    (x + 4,     y + T - 4)]
    elif direcao == "CIMA":     pts = [(x + 4,     y + 4),    (x + T - 4, y + 4)]
    else:                       pts = [(x + 4,     y + T - 4),(x + T - 4, y + T - 4)]
    for o in pts:
        pygame.draw.circle(surf, C.COBRA_OLHO,   o, r_olho)
        pygame.draw.circle(surf, C.COBRA_PUPILA, o, r_pupila)