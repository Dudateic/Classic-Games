import pygame
import sys
from entities.entities import Cobra


def processar_eventos(cobra: Cobra) -> str | None:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_p:
                return "PAUSAR"
            elif ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif ev.key == pygame.K_UP    or ev.key == pygame.K_w:
                cobra.definir_direcao("CIMA")
            elif ev.key == pygame.K_DOWN  or ev.key == pygame.K_s:
                cobra.definir_direcao("BAIXO")
            elif ev.key == pygame.K_LEFT  or ev.key == pygame.K_a:
                cobra.definir_direcao("ESQUERDA")
            elif ev.key == pygame.K_RIGHT or ev.key == pygame.K_d:
                cobra.definir_direcao("DIREITA")

    return None