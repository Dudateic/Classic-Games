from __future__ import annotations
import pygame
import config.config as C


def painel(surf: pygame.Surface, x: int, y: int, w: int, h: int,
           cor_borda: tuple | None = None, alpha: int = 200,
           radius: int = 10) -> None:
    """Painel semitransparente com borda e brilho interno no topo."""
    fundo = pygame.Surface((w, h), pygame.SRCALPHA)
    fundo.fill((8, 10, 20, alpha))
    surf.blit(fundo, (x, y))

    borda = cor_borda or C.COR_HUD_BORDA
    pygame.draw.rect(surf, borda, (x, y, w, h), width=2, border_radius=radius)

    brilho = pygame.Surface((w - 20, 2), pygame.SRCALPHA)
    brilho.fill((*borda[:3], 60))
    surf.blit(brilho, (x + 10, y + 5))


def barra_progresso(surf: pygame.Surface, x: int, y: int, w: int, h: int,
                    proporcao: float, cor: tuple,
                    cor_fundo: tuple = (10, 10, 20),
                    radius: int = 4) -> None:
    """Barra de progresso horizontal com cantos arredondados."""
    pygame.draw.rect(surf, cor_fundo, (x, y, w, h), border_radius=radius)
    pygame.draw.rect(surf, C.COR_HUD_BORDA, (x, y, w, h), width=1, border_radius=radius)
    if proporcao > 0:
        fill_w = max(radius * 2, int(w * min(1.0, proporcao)))
        pygame.draw.rect(surf, cor, (x, y, fill_w, h), border_radius=radius)


def separador(surf: pygame.Surface, x1: int, x2: int, y: int,
              cor: tuple | None = None, alpha: int = 120) -> None:
    """Linha horizontal semitransparente."""
    cor = cor or C.COR_HUD_BORDA
    linha = pygame.Surface((x2 - x1, 1), pygame.SRCALPHA)
    linha.fill((*cor, alpha))
    surf.blit(linha, (x1, y))


def destaque_linha(surf: pygame.Surface, x: int, y: int, w: int, h: int,
                   cor: tuple = (60, 140, 220), alpha: int = 40,
                   radius: int = 6) -> None:
    """Fundo de destaque semitransparente para linhas selecionadas."""
    hl = pygame.Surface((w, h), pygame.SRCALPHA)
    hl.fill((*cor, alpha))
    surf.blit(hl, (x, y))
    pygame.draw.rect(surf, C.COR_HUD_BORDA, (x, y, w, h), width=1, border_radius=radius)