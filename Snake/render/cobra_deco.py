from __future__ import annotations
import math
import pygame
import config.config as C


def desenhar(surf: pygame.Surface, frame: int,
             cx: int | None = None, cy_inicio: int = 170,
             comprimento: int = 16) -> None:

    T  = C.TAMANHO_CELULA
    cx = cx or C.LARGURA_TELA // 2

    for i in range(comprimento):
        ox     = cx + int(math.sin(frame * 0.04 + i * 0.45) * (60 - i * 2.2))
        oy     = cy_inicio + i * T
        t_norm = i / max(comprimento - 1, 1)

        r = int(C.COBRA_CABECA[0] * (1 - t_norm) + C.COBRA_CORPO_2[0] * t_norm)
        g = int(C.COBRA_CABECA[1] * (1 - t_norm) + C.COBRA_CORPO_2[1] * t_norm)
        b = int(C.COBRA_CABECA[2] * (1 - t_norm) + C.COBRA_CORPO_2[2] * t_norm)
        cor = (r, g, b)

        rx   = ox - T // 2
        rect = pygame.Rect(rx + 1, oy + 1, T - 2, T - 2)

        sombra = pygame.Rect(rx + 3, oy + 3, T - 2, T - 2)
        pygame.draw.rect(surf, (0, 0, 0), sombra, border_radius=4)

        pygame.draw.rect(surf, cor,          rect, border_radius=4)
        pygame.draw.rect(surf, C.COBRA_BORDA, rect, width=1, border_radius=4)

        if i == 0:
            for o in [(rx + T - 5, oy + 5), (rx + T - 5, oy + T - 5)]:
                pygame.draw.circle(surf, C.COBRA_OLHO,   o, T // 5)
                pygame.draw.circle(surf, C.COBRA_PUPILA, o, T // 8)