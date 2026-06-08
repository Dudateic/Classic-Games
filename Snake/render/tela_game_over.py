from __future__ import annotations
import math
import pygame
import config.config as C
import render.texto as Texto
import render.ui as UI
from render.fundo import grade_simples
from render.tela_novo_recorde import TelaNovoRecorde


class TelaGameOver:
    def __init__(self, fontes, particulas) -> None:
        self._pt = particulas
        self._tela_recorde = TelaNovoRecorde(fontes, particulas)

    def executar(self, surf: pygame.Surface, clock: pygame.time.Clock, flip,
                 pontuacao: int, highscore: int, nivel: int,
                 nome_jogador: str = "") -> str:
        """Retorna: 'JOGAR' | 'RANKING' | 'MENU'"""
        frame = 0
        opcoes = ["JOGAR NOVAMENTE", "VER RANKING", "MENU PRINCIPAL"]
        retornos = ["JOGAR", "RANKING", "MENU"]
        selecionado = 0
        novo_record = pontuacao >= highscore and pontuacao > 0
        cx = C.LARGURA_TELA // 2

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_UP, pygame.K_w):
                        selecionado = (selecionado - 1) % len(opcoes)
                    elif ev.key in (pygame.K_DOWN, pygame.K_s):
                        selecionado = (selecionado + 1) % len(opcoes)
                    elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return retornos[selecionado]
                    elif ev.key == pygame.K_ESCAPE:
                        return "MENU"

            grade_simples(surf)
            self._pt.atualizar()
            self._pt.desenhar(surf)

            Texto.desenhar(surf, "GAME OVER", 200, C.VERMELHO, cx, 120, centralizar=True)

            pw_r, ph_r = 520, 160
            px_r = cx - pw_r // 2
            py_r = 180
            
            cols = [
                ("PONTOS", str(pontuacao), C.COR_HUD_DESTAQUE),
                ("NIVEL", str(nivel), C.COR_FRUTA_BOOST),
                ("RECORDE", str(highscore), C.AMARELO),
            ]
            pw_r = 660
            px_r = cx - pw_r // 2  
            py_r = 220
            col_w = pw_r // len(cols)

            for i, (lbl, val, cor) in enumerate(cols):
                x = px_r + col_w * i + col_w // 2
                Texto.desenhar(surf, lbl, 26.5, C.COR_HUD_TEXTO, x, py_r + 25, centralizar=True)
                Texto.desenhar(surf, val, 26.5, cor, x, py_r + 80, centralizar=True)

            novo_record = pontuacao >= highscore and pontuacao > 0
            if novo_record:
                return self._tela_recorde.executar(
                    surf, clock, flip,
                    pontuacao=pontuacao,
                    highscore_anterior=highscore,
                    nivel=nivel,
                    nome_jogador=nome_jogador,
    )
            pw, ph = 380, len(opcoes) * 50 + 20
            px = cx - pw // 2
            py = 370

            for i, op in enumerate(opcoes):
                iy = py + 20 + i * 50
                if i == selecionado:
                    Texto.desenhar(surf, f"[ {op} ]", 26.5, C.AMARELO, cx, iy, centralizar=True)
                else:
                    Texto.desenhar(surf, op, 26.5, C.COR_HUD_TEXTO, cx, iy, centralizar=True)


            flip()
            clock.tick(C.FPS_BASE)
            frame += 1