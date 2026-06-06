import pygame, sys
from entities.entities import Cobra

def processar_eventos(cobra: Cobra):
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_p:
                return "PAUSAR"
            elif ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            elif ev.key == pygame.K_UP:
                cobra.definir_direcao("CIMA")
            elif ev.key == pygame.K_DOWN:
                cobra.definir_direcao("BAIXO")
            elif ev.key == pygame.K_LEFT:
                cobra.definir_direcao("ESQUERDA")
            elif ev.key == pygame.K_RIGHT:
                cobra.definir_direcao("DIREITA")
    return None