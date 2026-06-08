from __future__ import annotations
import pygame
import config.config as C
from . import fontes as Fontes
from . import texto as Texto
from . import ui as UI


def desenhar(surf: pygame.Surface, estado, frame: int) -> None:
    ox, W, H = C.LARGURA_JOGO, C.LARGURA_HUD, C.ALTURA

    _fundo(surf, ox, W, H, frame)
    _stats(surf, ox, W, estado)
    _boost(surf, ox, W, estado)
    _mensagem(surf, ox, W, H, estado)
    _legenda(surf, ox, W, H)
    _rodape(surf, ox, W, H)


def _fundo(surf, ox, W, H, frame):
    pygame.draw.rect(surf, C.COR_HUD_FUNDO, (ox, 0, W, H))
    pygame.draw.line(surf, C.COR_HUD_BORDA, (ox, 0), (ox, H), 1)
    
    Texto.desenhar(surf, "SNAKE", 26, C.COR_HUD_DESTAQUE, ox + W // 2, 25, centralizar=True)
    UI.separador(surf, ox + 20, ox + W - 20, 75)


def _stats(surf, ox, W, estado):
    y, dy = 95, 60
    _bloco(surf, ox, W, y,          "PONTOS",  str(estado.pontuacao),  C.COR_HUD_DESTAQUE)
    _bloco(surf, ox, W, y + dy,     "RECORDE", str(estado.highscore),  C.AMARELO)
    _bloco(surf, ox, W, y + dy * 2, "NIVEL",   str(estado.nivel),      C.COR_FRUTA_BOOST)
    _bloco(surf, ox, W, y + dy * 3, "TAMANHO", str(len(estado.cobra)), C.VERDE_UI)
    
    UI.separador(surf, ox + 20, ox + W - 20, y + dy * 4 - 10)


def _boost(surf, ox, W, estado):
    y = 100 + 60 * 4 + 10
    Texto.desenhar(surf, "SPEED BOOST", 16, C.COR_HUD_LABEL, ox + W // 2, y - 10, centralizar=True)
    
    bx, by, bw, bh = ox + 20, y + 22, W - 40, 10
    prop = estado.boost_restante / C.DURACAO_BOOST if estado.boost_ativo else 0.0
    UI.barra_progresso(surf, bx, by - 5, bw, bh, prop, C.COR_FRUTA_BOOST)
    
    if estado.boost_ativo:
        Texto.desenhar(surf, f"{estado.boost_restante:.1f} SEG", 17, C.COR_HUD_TEXTO,
                       ox + W // 2, by + 16, centralizar=True)
    else:
        Texto.desenhar(surf, "INATIVO", 16, C.CINZA, ox + W // 2, by + 17, centralizar=True)


def _mensagem(surf, ox, W, H, estado):
    if estado.mensagem_timer > 0:
        alpha = min(255, estado.mensagem_timer * 6)
        msg = Fontes.med().render(estado.mensagem_texto, True, estado.mensagem_cor)
        msg.set_alpha(alpha)
        surf.blit(msg, ((ox + W  // 2) + 8 - (msg.get_width() // 2), H - 300))


def _legenda(surf, ox, W, H):
    y = H - 220
    UI.separador(surf, ox + 20, ox + W - 20, y - 30)
    Texto.desenhar(surf, "ITENS DE JOGO", 16, C.COR_HUD_LABEL, ox + W // 2, y - 20, centralizar=True)

    itens = [
        (C.COR_FRUTA_RUIM,   "   RUIM     -1"),
        (C.COR_FRUTA_BOA[0], "   BOA      +1"),
        (C.COR_FRUTA_BOA[1], "   BOA      +2"),
        (C.COR_FRUTA_BOA[2], "   BOA      +3"),

        (C.COR_FRUTA_BOA[3], "   BOA      +4"),
        (C.COR_FRUTA_OURO,   "   OURO     +5"),
        (C.COR_FRUTA_BOOST,  "   SPEED    +5s"),
    ]

    for i, (cor, label) in enumerate(itens):
        iy = y + 8 + i * 22
        pygame.draw.rect(surf, cor, (ox + 55, iy + 2, 10, 10), border_radius=1)
        Texto.desenhar(surf, label, 16, C.COR_HUD_TEXTO, ox + W // 2, iy, centralizar=True)


def _rodape(surf, ox, W, H):
    UI.separador(surf, ox + 20, ox + W - 20, H - 45)
    Texto.desenhar(surf, "[ P ] PAUSAR", 16, C.COR_HUD_LABEL,
                   ox + W // 2, H - 32, centralizar=True)


def _bloco(surf, ox, W, y, label, valor, cor_valor):
    Texto.desenhar(surf, label, 17, C.COR_HUD_LABEL,  ox + W // 2, y - 10,      centralizar=True)
    Texto.desenhar(surf, valor, 19, cor_valor,        ox + W // 2, y + 15, centralizar=True)