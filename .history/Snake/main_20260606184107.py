import pygame
import sys
import config.config as C
from entities.entities import Cobra, Fruta, Particula, gerar_fruta, criar_particulas
from engine.game_state import EstadoJogo, salvar_entrada_ranking, carregar_ranking
from engine.input_handler import processar_eventos
from render.renderer import (
    desenhar_grade, desenhar_cobra, desenhar_frutas,
    desenhar_particulas, desenhar_hud,
    tela_inicio, tela_pause, tela_game_over,
    tela_digitar_nome, tela_ranking,
)


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

    proxima = "MENU"
    nome_jogador = ""

    while True:
        if proxima == "MENU":
            acao = tela_inicio(surf, clock, flip)
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
                    tela_pause(surf, clock, flip)

                estado.tick()
                _render(surf, estado, frame)
                flip()

            # fim de jogo
            nome_jogador = ""
            if estado.pontuacao > 0:
                nome_jogador = tela_digitar_nome(surf, clock, flip, estado.pontuacao)
                salvar_entrada_ranking(nome_jogador, estado.pontuacao, estado.nivel)

            resultado = tela_game_over(
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
            resultado = tela_ranking(surf, clock, flip, ranking, destaque_nome=nome_jogador)
            if resultado == "JOGAR":
                proxima = "JOGAR"
            else:
                proxima = "MENU"


def _render(surf, estado, frame):
    desenhar_grade(surf, frame)
    desenhar_particulas(surf, estado.particulas)
    desenhar_frutas(surf, estado.frutas)
    desenhar_cobra(surf, estado.cobra, estado.boost_ativo, frame)
    desenhar_hud(surf, estado, frame)


if __name__ == "__main__":
    main()