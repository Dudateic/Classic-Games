from __future__ import annotations
import pygame
import config.config as C
import render.texto as Texto
import render.ui as UI
from render.fundo import grade_simples

class TelaNome:
    def __init__(self, fontes, particulas) -> None:
        self._pt = particulas

    
    def executar(self, surf: pygame.Surface, clock: pygame.time.Clock,
                 flip, pontuacao: int) -> str:
        frame = 0
        nome = ""
        MAX_CAR = 10
        cx = C.LARGURA_TELA // 2
        
        pw, ph = 500, 240
        px = cx - pw // 2
        py = C.ALTURA // 2 - ph // 2

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN and nome.strip():
                        return nome.strip().upper()
                    elif ev.key == pygame.K_ESCAPE:
                        return "CLASSIC"
                    elif ev.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        if len(nome) < MAX_CAR and ev.unicode.isalpha():
                            nome += ev.unicode.upper()

            grade_simples(surf)
            self._pt.atualizar()
            self._pt.desenhar(surf)
            
            Texto.desenhar(surf, "REGISTRO DE RECORD", 36, C.AMARELO, cx, py + 30, centralizar=True)
            Texto.desenhar(surf, f"SUA PONTUACAO FINAL: {pontuacao} PONTOS", 20 , C.COR_HUD_TEXTO, cx, py + 90, centralizar=True)

            bx, by, bw, bh = cx - 180, py + 135, 360, 40
            pygame.draw.rect(surf, (10, 10, 12), (bx, by, bw, bh), border_radius=4)
            pygame.draw.rect(surf, C.AMARELO, (bx, by, bw, bh), width=1, border_radius=4)
            
            cursor = "_" if (frame // 20) % 2 == 0 else " "
            Texto.desenhar(surf, nome + cursor, 26, C.BRANCO, cx, by + 8, centralizar=True)

            Texto.desenhar(surf, "ENTER - CONFIRMAR   ESC - IGNORAR",
                           17, C.COR_HUD_TEXTO, cx, py + ph - 30, centralizar=True)

            flip()
            clock.tick(C.FPS_BASE)
            frame += 1