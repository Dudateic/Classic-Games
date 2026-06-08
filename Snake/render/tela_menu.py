from __future__ import annotations
import math
import random
import pygame
import config.config as C
import render.fontes as Fontes
import render.texto as Texto
import render.ui as UI
from entities.entities import Cobra, Fruta, gerar_fruta
from render.fundo import grade_brilhante

class TelaMenu:
    def __init__(self, fontes, particulas) -> None:
        self._pt = particulas
        self.reiniciar_demo()

    def reiniciar_demo(self) -> None:
        """Inicializa a cobra de demonstração que joga sozinha no menu."""
        self.demo_cobra = Cobra()
        self.demo_frutas: list[Fruta] = []
        for _ in range(4):
            self.demo_frutas.append(self._gerar_fruta_menu())
        self.demo_tick_timer = 0

    def _gerar_fruta_menu(self) -> Fruta:
        """Gera frutas considerando a largura total da tela no menu."""
        cols = C.LARGURA_TELA // C.TAMANHO_CELULA
        rows = C.ALTURA // C.TAMANHO_CELULA
        ocupadas = set(self.demo_cobra.corpo) | {f.pos for f in self.demo_frutas}
        while True:
            x = random.randint(1, cols - 2) * C.TAMANHO_CELULA
            y = random.randint(1, rows - 2) * C.TAMANHO_CELULA
            if (x, y) not in ocupadas:
                tipo = random.choice(["bom", "boost", "ouro"])
                cor = C.COR_FRUTA_BOA[0] if tipo == "bom" else (C.COR_FRUTA_BOOST if tipo == "boost" else C.COR_FRUTA_OURO)
                return Fruta(tipo=tipo, pos=(x, y), cor=cor)

    def atualizar_ia_demo(self) -> None:
        """Algoritmo clássico de busca de caminho (Greedy Pathfinding) para a cobra do menu."""
        if not self.demo_cobra.viva:
            self.reiniciar_demo()
            return

        self.demo_tick_timer += 1
        if self.demo_tick_timer < 5:
            return
        self.demo_tick_timer = 0

        hx, hy = self.demo_cobra.cabeca
        if not self.demo_frutas:
            self.demo_frutas.append(self._gerar_fruta_menu())
            
        fruta_alvo = self.demo_frutas[0]
        fx, fy = fruta_alvo.pos

        opostos = {"CIMA": "BAIXO", "BAIXO": "CIMA", "ESQUERDA": "DIREITA", "DIREITA": "ESQUERDA"}
        deltas = {"CIMA": (0, -1), "BAIXO": (0, 1), "ESQUERDA": (-1, 0), "DIREITA": (1, 0)}
        
        direcoes_validas = []
        for d in ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]:
            if d == opostos[self.demo_cobra.direcao]:
                continue
            dx, dy = deltas[d]
            nx = (hx + dx * C.TAMANHO_CELULA) % C.LARGURA_TELA
            ny = (hy + dy * C.TAMANHO_CELULA) % C.ALTURA
            if (nx, ny) not in self.demo_cobra.corpo[:-1]:
                direcoes_validas.append((d, nx, ny))

        if not direcoes_validas:
            self.demo_cobra.mover()
            return

        melhor_dir = direcoes_validas[0][0]
        menor_distancia = float("inf")
        
        for d, nx, ny in direcoes_validas:
            dist = abs(nx - fx) + abs(ny - fy)
            if dist < menor_distancia:
                menor_distancia = dist
                melhor_dir = d

        self.demo_cobra.definir_direcao(melhor_dir)
        self.demo_cobra.mover()

        cabeca = self.demo_cobra.cabeca
        novas_frutas = []
        comeu = False
        for f in self.demo_frutas:
            if f.pos == cabeca:
                self.demo_cobra.crescer(2)
                comeu = True
            else:
                novas_frutas.append(f)
        
        if comeu:
            self.demo_frutas = novas_frutas
            self.demo_frutas.append(self._gerar_fruta_menu())

    def desenhar_demo(self, surf: pygame.Surface) -> None:
        """Renderiza discretamente a simulação em segundo plano."""
        T = C.TAMANHO_CELULA
        for f in self.demo_frutas:
            rect = pygame.Rect(f.pos[0] + 3, f.pos[1] + 3, T - 6, T - 6)
            s = pygame.Surface((T, T), pygame.SRCALPHA)
            pygame.draw.rect(s, (*f.cor, 100), (3, 3, T - 6, T - 6), border_radius=4)
            surf.blit(s, f.pos)

        for i, (x, y) in enumerate(self.demo_cobra.corpo):
            t_norm = i / max(len(self.demo_cobra.corpo) - 1, 1)
            r = int(C.COBRA_CABECA[0] * (1 - t_norm) + C.COBRA_CORPO_2[0] * t_norm)
            g = int(C.COBRA_CABECA[1] * (1 - t_norm) + C.COBRA_CORPO_2[1] * t_norm)
            b = int(C.COBRA_CABECA[2] * (1 - t_norm) + C.COBRA_CORPO_2[2] * t_norm)
            
            s = pygame.Surface((T, T), pygame.SRCALPHA)
            pygame.draw.rect(s, (r, g, b, 70), (1, 1, T - 2, T - 2), border_radius=4)
            surf.blit(s, (x, y))

    def executar(self, surf: pygame.Surface, clock: pygame.time.Clock, flip) -> str:
        """Retorna a opção selecionada: 'JOGAR' | 'RANKING' | 'SAIR'"""
        self._pt.resetar()
        self.reiniciar_demo()
        frame = 0
        opcoes = ["JOGAR", "RANKING", "SAIR"]
        selecionado = 0
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
                        return opcoes[selecionado]
                    elif ev.key == pygame.K_ESCAPE:
                        return "SAIR"

            grade_brilhante(surf, frame)
            self.atualizar_ia_demo()
            self.desenhar_demo(surf)

            self._pt.atualizar()
            self._pt.desenhar(surf)

            Texto.desenhar(surf, "S N A K E", 200, C.AMARELO, cx, 180, centralizar=True)

            for i, op in enumerate(opcoes):
                iy = 300 + i * 60
                if i == selecionado:
                    Texto.desenhar(surf, f"[ {op} ]", 26.5, C.BRANCO, cx, iy, centralizar=True)
                else:
                    Texto.desenhar(surf, op, 26.5, C.COR_HUD_TEXTO, cx, iy, centralizar=True)



            flip()
            clock.tick(C.FPS_BASE)
            frame += 1