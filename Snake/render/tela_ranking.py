from __future__ import annotations
import pygame
import config.config as C

class TelaRanking:
    def __init__(self, fontes=None, particulas=None) -> None:
        pass

    def executar(self, surf: pygame.Surface, clock: pygame.time.Clock, flip, ranking: list[dict], destaque_nome: str = "") -> str:
        cx = C.LARGURA_TELA // 2
        fonte_tit = pygame.font.SysFont("monospace", 50, bold=True)
        fonte_txt = pygame.font.SysFont("monospace", 22, bold=True)

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        return "MENU"

            surf.fill(C.COR_FUNDO)

            tit = fonte_tit.render("TOP SCORES", True, C.AMARELO)
            surf.blit(tit, (cx - tit.get_width() // 2, 50))
            pygame.draw.line(surf, C.AMARELO, (cx - 200, 110), (cx + 200, 110), 1)

            col_lbl = fonte_txt.render(f"{'POS':<5}{'JOGADOR':<15}{'PONTOS':<10}{'NIVEL':<5}", True, C.COR_HUD_LABEL)
            surf.blit(col_lbl, (cx - col_lbl.get_width() // 2, 140))
            pygame.draw.line(surf, C.COR_HUD_LABEL, (cx - col_lbl.get_width() // 2, 165), (cx + col_lbl.get_width() // 2, 165), 1)

            y_item = 185
            if not ranking:
                aviso = fonte_txt.render("NENHUM REGISTRO ENCONTRADO", True, C.BRANCO)
                surf.blit(aviso, (cx - aviso.get_width() // 2, y_item + 40))
            else:
                for idx, entrada in enumerate(ranking[:10]):
                    pos_str = f"{idx + 1}."
                    nome = entrada.get("nome", "ANONIMO")
                    pts = str(entrada.get("pontuacao", 0))
                    nv = str(entrada.get("nivel", 1))

                    linha_texto = f"{pos_str:<5}{nome:<15}{pts:<10}{nv:<5}"
                    
                    cor_linha = C.VERDE_UI if nome == destaque_nome and destaque_nome else C.BRANCO
                    
                    item_render = fonte_txt.render(linha_texto, True, cor_linha)
                    surf.blit(item_render, (cx - item_render.get_width() // 2, y_item))
                    y_item += 35

            lbl_voltar = fonte_txt.render("PRESSIONE ESPACO OU ESC PARA VOLTAR", True, C.COR_HUD_LABEL)
            surf.blit(lbl_voltar, (cx - lbl_voltar.get_width() // 2, C.ALTURA - 60))

            flip()
            clock.tick(C.FPS_BASE)