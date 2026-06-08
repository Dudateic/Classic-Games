import pygame
import sys
import config.config as C
from entities.entities import Cobra, Fruta, Particula, gerar_fruta, criar_particulas
from engine.game_state import EstadoJogo, salvar_entrada_ranking, carregar_ranking
from engine.input_handler import processar_eventos

import render.fontes as Fontes
import render.particulas_menu as ParticulasMenu

from render.tela_menu import TelaMenu
from render.tela_pausa import TelaPausa
from render.tela_game_over import TelaGameOver
from render.tela_nome import TelaNome
from render.tela_ranking import TelaRanking 
from render.jogo import desenhar_tudo as desenhar_grade

import render.hub as Hud 

def main():
    pygame.init()

    info = pygame.display.Info()
    sw, sh = info.current_w, info.current_h
    tela_real = pygame.display.set_mode((sw, sh), pygame.FULLSCREEN)
    pygame.display.set_caption(C.TITULO)

    surf = pygame.Surface((C.LARGURA_TELA, C.ALTURA))

    escala = min(sw / C.LARGURA_TELA, sh / C.ALTURA)
    w_scaled = int(C.LARGURA_TELA * escala)
    h_scaled = int(C.ALTURA * escala)
    offset_x = (sw - w_scaled) // 2
    offset_y = (sh - h_scaled) // 2

    clock = pygame.time.Clock()

    def flip():
        tela_real.fill((0, 0, 0))
        scaled = pygame.transform.scale(surf, (w_scaled, h_scaled))
        tela_real.blit(scaled, (offset_x, offset_y))
        pygame.display.flip()

    Fontes.init()

    menu_manager = TelaMenu(Fontes, ParticulasMenu)
    game_over_manager = TelaGameOver(Fontes, ParticulasMenu)
    nome_manager = TelaNome(Fontes, ParticulasMenu)
    ranking_manager = TelaRanking(Fontes, ParticulasMenu) 
    pausa_manager = TelaPausa(Fontes)

    proxima = "MENU"
    nome_jogador = ""

    while True:
        if proxima == "MENU":
            acao = menu_manager.executar(surf, clock, flip)
            if acao == "SAIR":
                pygame.quit(); sys.exit()
            elif acao == "RANKING":
                proxima = "RANKING"
            else:
                proxima = "JOGAR"

        elif proxima == "JOGAR":
            estado = EstadoJogo()
            frame  = 0

            while estado.cobra.viva:
                clock.tick(C.FPS_BASE)
                frame += 1

                acao = processar_eventos(estado.cobra)
                if acao == "PAUSAR":
                    _render(surf, estado, frame)
                    flip()
                    pausa_manager.executar(surf, clock, flip)

                estado.tick()
                _render(surf, estado, frame)
                flip()

            nome_jogador = ""
            if estado.pontuacao > 0:
                nome_jogador = nome_manager.executar(surf, clock, flip, estado.pontuacao)
                salvar_entrada_ranking(nome_jogador, estado.pontuacao, estado.nivel)

            resultado = game_over_manager.executar(
                surf, clock, flip,
                estado.pontuacao, estado.highscore, estado.nivel,
                nome_jogador
            )

            if resultado == "JOGAR":
                proxima = "JOGAR"
            elif resultado == "RANKING":
                proxima = "RANKING"
            else:
                proxima = "MENU"

        elif proxima == "RANKING":
            ranking = carregar_ranking()
            resultado = ranking_manager.executar(surf, clock, flip, ranking, destaque_nome=nome_jogador)
            if resultado == "JOGAR":
                proxima = "JOGAR"
            else:
                proxima = "MENU"

def _render(surf, estado, frame):
    desenhar_grade(surf, estado, frame)
    Hud.desenhar(surf, estado, frame)

if __name__ == "__main__":
    main()