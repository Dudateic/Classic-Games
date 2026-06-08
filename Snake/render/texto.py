from __future__ import annotations
import math
import pygame
import render.fontes as Fontes


def desenhar(surf: pygame.Surface, txt: str, tamanho: int, cor: tuple,
             x: int, y: int, centralizar: bool = False, alpha: int = 255) -> None:
    """Texto simples, com suporte a centralização e transparência."""
    rendered = Fontes.get(tamanho).render(txt, True, cor)
    if alpha < 255:
        rendered.set_alpha(alpha)
    rx = x - rendered.get_width() // 2 if centralizar else x
    surf.blit(rendered, (rx, y))


def desenhar_sombra(surf: pygame.Surface, txt: str, tamanho: int, cor: tuple,
                    x: int, y: int, centralizar: bool = False, offset: int = 3) -> None:
    """Texto com sombra deslocada atrás."""
    fonte = Fontes.get(tamanho)
    sombra    = fonte.render(txt, True, (0, 0, 0))
    principal = fonte.render(txt, True, cor)
    rx = x - principal.get_width() // 2 if centralizar else x
    surf.blit(sombra,    (rx + offset, y + offset))
    surf.blit(principal, (rx, y))


def desenhar_glow(surf: pygame.Surface, txt: str, tamanho: int, cor: tuple,
                  x: int, y: int, centralizar: bool = False,
                  glow_radius: int = 4) -> None:
    """Texto com halo luminoso ao redor."""
    fonte = Fontes.get(tamanho)
    base  = fonte.render(txt, True, cor)
    glow  = fonte.render(txt, True, cor)

    if centralizar:
        x -= base.get_width() // 2

    for dx in range(-glow_radius, glow_radius + 1, 2):
        for dy in range(-glow_radius, glow_radius + 1, 2):
            alpha_glow = max(0, 80 - int(math.hypot(dx, dy) * 20))
            if alpha_glow <= 0:
                continue
            tmp = glow.copy()
            tmp.set_alpha(alpha_glow)
            surf.blit(tmp, (x + dx, y + dy))

    surf.blit(base, (x, y))