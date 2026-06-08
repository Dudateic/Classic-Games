from __future__ import annotations
import pygame
import config.config as C

class TelaPausa:
    def __init__(self, fontes) -> None:
        self._fontes = fontes

    def executar(self, surf: pygame.Surface, clock: pygame.time.Clock, flip) -> None:
        fonte_tit = pygame.font.SysFont("monospace", 36, bold=True)
        fonte_txt = pygame.font.SysFont("monospace", 20, bold=True)
        
        lbl_tit = fonte_tit.render("PAUSA", True, C.AMARELO)
        lbl_sub = fonte_txt.render("PRESSIONE P PARA RETORNAR", True, C.COR_HUD_LABEL)
        
        cx, cy = C.LARGURA_TELA // 2, C.ALTURA // 2
        
        overlay = pygame.Surface((C.LARGURA_TELA, C.ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        surf.blit(overlay, (0, 0))
        
        surf.blit(lbl_tit, (cx - lbl_tit.get_width() // 2, cy - 40))
        surf.blit(lbl_sub, (cx - lbl_sub.get_width() // 2, cy + 15))
        
        flip()
        
        pausado = True
        while pausado:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_p, pygame.K_ESCAPE):
                        pausado = False
            
            clock.tick(C.FPS_BASE)