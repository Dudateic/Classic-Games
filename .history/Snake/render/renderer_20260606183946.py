from __future__ import annotations
import math
import pygame
import config.config as C
from entities.entities import Cobra, Fruta, Particula

_font_sm  = None
_font_lg  = None
_font_med = None
_font_xl  = None
_font_xs  = None

def _init_fonts():
    global _font_sm, _font_lg, _font_med, _font_xl, _font_xs
    if _font_sm is None:
        _font_xs  = pygame.font.SysFont("monospace", 14, bold=True)
        _font_sm  = pygame.font.SysFont("monospace", 18, bold=True)
        _font_lg  = pygame.font.SysFont("monospace", 48, bold=True)
        _font_med = pygame.font.SysFont("monospace", 26, bold=True)
        _font_xl  = pygame.font.SysFont("monospace", 72, bold=True)

def _fonte(tamanho: int) -> pygame.font.Font:
    _init_fonts()
    if tamanho <= 14: return _font_xs
    if tamanho <= 18: return _font_sm
    if tamanho <= 26: return _font_med
    if tamanho <= 48: return _font_lg
    return _font_xl

def _texto(surf, txt, tamanho, cor, x, y, centralizar=False, alpha=255):
    rendered = _fonte(tamanho).render(txt, True, cor)
    if alpha < 255:
        rendered.set_alpha(alpha)
    if centralizar:
        x -= rendered.get_width() // 2
    surf.blit(rendered, (x, y))

def _texto_sombra(surf, txt, tamanho, cor, x, y, centralizar=False):
    sombra = _fonte(tamanho).render(txt, True, (0, 0, 0))
    rx = x - (sombra.get_width() // 2 if centralizar else 0)
    surf.blit(sombra, (rx + 3, y + 3))
    principal = _fonte(tamanho).render(txt, True, cor)
    surf.blit(principal, (rx, y))

def _painel_vidro(surf, x, y, w, h, cor_borda=None):
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((10, 12, 20, 190))
    surf.blit(panel, (x, y))
    borda = cor_borda or C.COR_HUD_BORDA
    pygame.draw.rect(surf, borda, (x, y, w, h), width=2, border_radius=8)
    brilho_surf = pygame.Surface((w - 20, 2), pygame.SRCALPHA)
    brilho_surf.fill((*borda, 80))
    surf.blit(brilho_surf, (x + 10, y + 4))

def _grade_simples(surf):
    surf.fill(C.COR_FUNDO)
    T = C.TAMANHO_CELULA
    for x in range(0, C.LARGURA_TELA, T):
        pygame.draw.line(surf, C.COR_GRADE, (x, 0), (x, C.ALTURA))
    for y in range(0, C.ALTURA, T):
        pygame.draw.line(surf, C.COR_GRADE, (0, y), (C.LARGURA_TELA, y))

def _cobra_decorativa(surf, frame):
    T = C.TAMANHO_CELULA
    comprimento = 14
    cx = C.LARGURA_TELA // 2
    cy = 170
    for i in range(comprimento):
        ox = cx + int(math.sin(frame * 0.04 + i * 0.5) * (55 - i * 2))
        oy = cy + i * T
        t_norm = i / max(comprimento - 1, 1)
        r = int(C.COBRA_CABECA[0] * (1-t_norm) + C.COBRA_CORPO_2[0] * t_norm)
        g = int(C.COBRA_CABECA[1] * (1-t_norm) + C.COBRA_CORPO_2[1] * t_norm)
        b = int(C.COBRA_CABECA[2] * (1-t_norm) + C.COBRA_CORPO_2[2] * t_norm)
        rx = ox - T // 2
        rect = pygame.Rect(rx + 1, oy + 1, T - 2, T - 2)
        pygame.draw.rect(surf, (r, g, b), rect, border_radius=3)
        pygame.draw.rect(surf, C.COBRA_BORDA, rect, width=1, border_radius=3)
        if i == 0:
            for o in [(rx + T - 4, oy + 4), (rx + T - 4, oy + T - 4)]:
                pygame.draw.circle(surf, C.COBRA_OLHO, o, T // 5)
                pygame.draw.circle(surf, C.COBRA_PUPILA, o, T // 8)


def desenhar_grade(surf: pygame.Surface, tick: int) -> None:
    surf.fill(C.COR_FUNDO)
    T = C.TAMANHO_CELULA
    for x in range(0, C.LARGURA_JOGO, T):
        pygame.draw.line(surf, C.COR_GRADE, (x, 0), (x, C.ALTURA))
    for y in range(0, C.ALTURA, T):
        pygame.draw.line(surf, C.COR_GRADE, (0, y), (C.LARGURA_JOGO, y))

def desenhar_cobra(surf, cobra: Cobra, boost: bool, frame: int) -> None:
    T = C.TAMANHO_CELULA
    n = len(cobra.corpo)
    for i, (x, y) in enumerate(cobra.corpo):
        t_norm = i / max(n - 1, 1)
        if boost:
            cor_base = C.ARCO_IRIS_NEON[(frame // 2 + i) % len(C.ARCO_IRIS_NEON)]
        else:
            r = int(C.COBRA_CABECA[0] * (1-t_norm) + C.COBRA_CORPO_2[0] * t_norm)
            g = int(C.COBRA_CABECA[1] * (1-t_norm) + C.COBRA_CORPO_2[1] * t_norm)
            b = int(C.COBRA_CABECA[2] * (1-t_norm) + C.COBRA_CORPO_2[2] * t_norm)
            cor_base = (r, g, b)
        rect = pygame.Rect(x + 1, y + 1, T - 2, T - 2)
        pygame.draw.rect(surf, cor_base, rect, border_radius=3)
        pygame.draw.rect(surf, C.COBRA_BORDA, rect, width=1, border_radius=3)
        if i == 0:
            _desenhar_olhos(surf, x, y, cobra.direcao)

def _desenhar_olhos(surf, x, y, direcao):
    T = C.TAMANHO_CELULA
    r_olho, r_pupila = T // 5, T // 8
    if direcao == "DIREITA":   pts = [(x+T-4, y+4),   (x+T-4, y+T-4)]
    elif direcao == "ESQUERDA": pts = [(x+4,   y+4),   (x+4,   y+T-4)]
    elif direcao == "CIMA":     pts = [(x+4,   y+4),   (x+T-4, y+4)]
    else:                       pts = [(x+4,   y+T-4), (x+T-4, y+T-4)]
    for o in pts:
        pygame.draw.circle(surf, C.COBRA_OLHO,   o, r_olho)
        pygame.draw.circle(surf, C.COBRA_PUPILA, o, r_pupila)

def desenhar_frutas(surf, frutas: list[Fruta]) -> None:
    T = C.TAMANHO_CELULA
    for fruta in frutas:
        x, y = fruta.pos
        rect = pygame.Rect(x+2, y+2, T-4, T-4)
        pygame.draw.rect(surf, fruta.cor, rect, border_radius=4)
        brilho = tuple(min(255, int(c * 1.5)) for c in fruta.cor)
        pygame.draw.circle(surf, brilho, (x+5, y+5), 2)
        pygame.draw.rect(surf, C.PRETO, rect, width=1, border_radius=4)

def desenhar_particulas(surf, particulas: list[Particula]) -> None:
    for p in particulas:
        r = int(p.raio)
        if r < 1: continue
        halo = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
        pygame.draw.circle(halo, (*p.cor, p.alpha), (r+1, r+1), r)
        surf.blit(halo, (int(p.x)-r-1, int(p.y)-r-1))

def desenhar_hud(surf, estado, frame: int) -> None:
    _init_fonts()
    ox, W, H = C.LARGURA_JOGO, C.LARGURA_HUD, C.ALTURA
    pygame.draw.rect(surf, C.COR_HUD_FUNDO, (ox, 0, W, H))
    pygame.draw.line(surf, C.COR_HUD_BORDA, (ox, 0), (ox, H), 2)
    brilho_t = 0.8 + 0.2 * math.sin(frame * 0.05)
    cor_t = tuple(int(c * brilho_t) for c in C.COR_HUD_DESTAQUE)
    _texto(surf, "SNAKE", 48, cor_t, ox + W//2, 16, centralizar=True)
    pygame.draw.line(surf, C.COR_HUD_BORDA, (ox+10, 76), (ox+W-10, 76), 1)
    y, dy = 90, 64
    _bloco(surf, ox, y,       "SCORE",  str(estado.pontuacao),  C.COR_HUD_DESTAQUE)
    _bloco(surf, ox, y+dy,    "RECORD", str(estado.highscore),  C.AMARELO)
    _bloco(surf, ox, y+dy*2,  "NIVEL",  str(estado.nivel),      C.COR_FRUTA_BOOST)
    _bloco(surf, ox, y+dy*3,  "SIZE",   str(len(estado.cobra)), C.VERDE_UI)
    pygame.draw.line(surf, C.COR_HUD_BORDA, (ox+10, y+dy*4+8), (ox+W-10, y+dy*4+8), 1)
    _barra_boost(surf, ox, y+dy*4+20, estado)
    _legenda(surf, ox, H-180)
    if estado.mensagem_timer > 0:
        alpha = min(255, estado.mensagem_timer * 6)
        rendered = _font_med.render(estado.mensagem_texto, True, estado.mensagem_cor)
        rendered.set_alpha(alpha)
        surf.blit(rendered, (ox + W//2 - rendered.get_width()//2, H - 270))
    _texto(surf, "[P] Pause", 18, C.COR_HUD_LABEL, ox + W//2, H-26, centralizar=True)

def _bloco(surf, ox, y, label, valor, cor_valor):
    W = C.LARGURA_HUD
    _texto(surf, label, 18, C.COR_HUD_LABEL, ox+W//2, y,    centralizar=True)
    _texto(surf, valor, 26, cor_valor,         ox+W//2, y+20, centralizar=True)

def _barra_boost(surf, ox, y, estado):
    W = C.LARGURA_HUD
    _texto(surf, "BOOST", 18, C.COR_HUD_LABEL, ox+W//2, y, centralizar=True)
    bx, by, bw, bh = ox+14, y+22, W-28, 12
    pygame.draw.rect(surf, C.PRETO, (bx, by, bw, bh), border_radius=4)
    pygame.draw.rect(surf, C.COR_HUD_BORDA, (bx, by, bw, bh), width=1, border_radius=4)
    if estado.boost_ativo:
        prop = max(0.0, min(1.0, estado.boost_restante / C.DURACAO_BOOST))
        pygame.draw.rect(surf, C.COR_FRUTA_BOOST, (bx, by, int(bw*prop), bh), border_radius=4)
        _texto(surf, f"{estado.boost_restante:.1f}s", 18, C.COR_HUD_TEXTO, ox+W//2, by+18, centralizar=True)
    else:
        _texto(surf, "OFF", 18, C.CINZA, ox+W//2, by+18, centralizar=True)

def _legenda(surf, ox, y):
    W = C.LARGURA_HUD
    pygame.draw.line(surf, C.COR_HUD_BORDA, (ox+10, y), (ox+W-10, y), 1)
    _texto(surf, "FRUTAS", 18, C.COR_HUD_LABEL, ox+W//2, y+4, centralizar=True)
    itens = [
        (C.COR_FRUTA_BOA[0], "Boa   +1"),
        (C.COR_FRUTA_RUIM,   "Ruim  -1"),
        (C.COR_FRUTA_BOOST,  "Boost +v"),
        (C.COR_FRUTA_OURO,   "Ouro  +5"),
    ]
    for i, (cor, label) in enumerate(itens):
        iy = y + 26 + i * 22
        pygame.draw.rect(surf, cor, (ox+14, iy, 12, 12), border_radius=2)
        _texto(surf, label, 18, C.COR_HUD_TEXTO, ox+32, iy-1)

# ─── TELAS ─────────────────────────────────────────────────────────────────────

def tela_inicio(surf, clock, flip):
    """Retorna: 'JOGAR' | 'RANKING' | 'SAIR'"""
    _init_fonts()
    frame = 0
    opcoes = ["JOGAR", "RANKING", "SAIR"]
    selecionado = 0
    cx = C.LARGURA_TELA // 2

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_UP, pygame.K_w):
                    selecionado = (selecionado - 1) % len(opcoes)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    selecionado = (selecionado + 1) % len(opcoes)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return opcoes[selecionado]
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit(); raise SystemExit

        _grade_simples(surf)
        _cobra_decorativa(surf, frame)

        brilho = 0.75 + 0.25 * math.sin(frame * 0.06)
        cor_titulo = tuple(int(c * brilho) for c in C.AMARELO)
        _texto_sombra(surf, "S N A K E", 72, cor_titulo, cx, 56, centralizar=True)

        pw, ph = 300, len(opcoes) * 56 + 24
        px = cx - pw // 2
        py = C.ALTURA // 2 - ph // 2 + 40
        _painel_vidro(surf, px, py, pw, ph)

        for i, op in enumerate(opcoes):
            iy = py + 20 + i * 56
            if i == selecionado:
                hl = pygame.Surface((pw - 16, 46), pygame.SRCALPHA)
                hl.fill((60, 140, 220, 40))
                surf.blit(hl, (px + 8, iy - 4))
                pygame.draw.rect(surf, C.COR_HUD_BORDA, (px+8, iy-4, pw-16, 46), width=1, border_radius=6)
                pulso = int(4 * abs(math.sin(frame * 0.1)))
                _texto(surf, ">", 26, C.AMARELO, px + 18 + pulso, iy + 4)
                cor_op = C.AMARELO
            else:
                cor_op = C.COR_HUD_TEXTO
            _texto(surf, op, 26, cor_op, cx, iy + 4, centralizar=True)

        flip()
        clock.tick(C.FPS_BASE)
        frame += 1


def tela_digitar_nome(surf, clock, flip, pontuacao):
    """Retorna o nome digitado."""
    _init_fonts()
    frame = 0
    nome = ""
    MAX = 12
    cx = C.LARGURA_TELA // 2
    pw, ph = 500, 220
    px, py = cx - pw // 2, C.ALTURA // 2 - ph // 2

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and nome.strip():
                    return nome.strip()
                elif ev.key == pygame.K_ESCAPE:
                    return "Anonimo"
                elif ev.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < MAX and ev.unicode.isprintable() and ev.unicode:
                        nome += ev.unicode

        _grade_simples(surf)
        _painel_vidro(surf, px, py, pw, ph, cor_borda=C.AMARELO)

        _texto(surf, "NOVO RECORDE!", 26, C.AMARELO, cx, py + 20, centralizar=True)
        _texto(surf, f"Pontuacao: {pontuacao}", 18, C.COR_HUD_DESTAQUE, cx, py + 58, centralizar=True)
        _texto(surf, "Digite seu nome:", 18, C.COR_HUD_LABEL, cx, py + 92, centralizar=True)

        bx, by, bw, bh = cx - 180, py + 118, 360, 36
        pygame.draw.rect(surf, (5, 8, 15), (bx, by, bw, bh), border_radius=4)
        pygame.draw.rect(surf, C.COR_HUD_BORDA, (bx, by, bw, bh), width=1, border_radius=4)
        cursor_vis = (frame // 20) % 2 == 0
        exibir = nome + ("|" if cursor_vis else " ")
        _texto(surf, exibir, 26, C.BRANCO, bx + 12, by + 4)


        flip()
        clock.tick(C.FPS_BASE)
        frame += 1


def tela_game_over(surf, clock, flip, pontuacao, highscore, nivel, nome_jogador=""):
    """Retorna: 'JOGAR' | 'MENU' | 'RANKING'"""
    _init_fonts()
    frame = 0
    opcoes = ["JOGAR NOVAMENTE", "VER RANKING", "MENU PRINCIPAL"]
    selecionado = 0
    novo_record = pontuacao >= highscore and pontuacao > 0
    cx = C.LARGURA_TELA // 2

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_UP, pygame.K_w):
                    selecionado = (selecionado - 1) % len(opcoes)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    selecionado = (selecionado + 1) % len(opcoes)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selecionado == 0: return "JOGAR"
                    if selecionado == 1: return "RANKING"
                    return "MENU"
                elif ev.key == pygame.K_ESCAPE:
                    return "MENU"

        _grade_simples(surf)

        brilho = 0.7 + 0.3 * abs(math.sin(frame * 0.07))
        cor_go = tuple(int(c * brilho) for c in C.VERMELHO)
        _texto_sombra(surf, "GAME  OVER", 72, cor_go, cx, 44, centralizar=True)

        if nome_jogador:
            _texto(surf, f"Jogador: {nome_jogador}", 18, C.COR_HUD_LABEL, cx, 134, centralizar=True)

        _painel_vidro(surf, cx - 220, 158, 440, 160)
        _texto(surf, "RESULTADO", 18, C.COR_HUD_LABEL, cx, 170, centralizar=True)
        pygame.draw.line(surf, C.COR_HUD_BORDA, (cx-180, 192), (cx+180, 192), 1)

        cols = [
            ("SCORE",  str(pontuacao), C.COR_HUD_DESTAQUE),
            ("NIVEL",  str(nivel),     C.COR_FRUTA_BOOST),
            ("RECORD", str(highscore), C.AMARELO),
        ]
        for i, (lbl, val, cor) in enumerate(cols):
            ix = cx - 140 + i * 140
            _texto(surf, lbl, 14, C.COR_HUD_LABEL, ix, 202, centralizar=True)
            _texto(surf, val, 26, cor,              ix, 222, centralizar=True)

        if novo_record:
            b2 = 0.6 + 0.4 * abs(math.sin(frame * 0.12))
            cor_hs = tuple(int(c * b2) for c in C.AMARELO)
            _texto(surf, "★  NOVO RECORDE!  ★", 26, cor_hs, cx, 286, centralizar=True)

        pw, ph = 340, len(opcoes) * 52 + 24
        px = cx - pw // 2
        py = C.ALTURA - ph - 70
        _painel_vidro(surf, px, py, pw, ph)

        for i, op in enumerate(opcoes):
            iy = py + 18 + i * 52
            if i == selecionado:
                hl = pygame.Surface((pw-16, 42), pygame.SRCALPHA)
                hl.fill((60, 140, 220, 40))
                surf.blit(hl, (px+8, iy-2))
                pygame.draw.rect(surf, C.COR_HUD_BORDA, (px+8, iy-2, pw-16, 42), width=1, border_radius=6)
                pulso = int(4 * abs(math.sin(frame * 0.1)))
                _texto(surf, ">", 18, C.AMARELO, px + 18 + pulso, iy + 8)
                cor_op = C.AMARELO
            else:
                cor_op = C.COR_HUD_TEXTO
            _texto(surf, op, 18, cor_op, cx, iy + 8, centralizar=True)

        flip()
        clock.tick(C.FPS_BASE)
        frame += 1


_MEDALHAS   = ["★", "✦", "◆"]
_COR_MEDALHA = [(255, 220, 50), (200, 200, 210), (200, 140, 80)]

def tela_ranking(surf, clock, flip, ranking: list[dict], destaque_nome=""):
    """Retorna: 'MENU' | 'JOGAR'"""
    _init_fonts()
    frame = 0
    cx = C.LARGURA_TELA // 2
    EXIBIR = 10

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_ESCAPE, pygame.K_m):
                    return "MENU"
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "JOGAR"

        _grade_simples(surf)

        brilho = 0.8 + 0.2 * math.sin(frame * 0.05)
        cor_tit = tuple(int(c * brilho) for c in C.AMARELO)
        _texto_sombra(surf, "RANKING", 72, cor_tit, cx, 26, centralizar=True)
        _texto(surf, "melhores pontuacoes", 14, C.COR_HUD_LABEL, cx, 112, centralizar=True)

        n_linhas = max(1, min(len(ranking), EXIBIR))
        pw, ph = 700, n_linhas * 48 + 80
        px, py = cx - pw // 2, 140

        _painel_vidro(surf, px, py, pw, ph)
        _texto(surf, "#",       14, C.COR_HUD_LABEL, px+24,  py+14)
        _texto(surf, "JOGADOR", 14, C.COR_HUD_LABEL, px+70,  py+14)
        _texto(surf, "SCORE",   14, C.COR_HUD_LABEL, px+390, py+14)
        _texto(surf, "NIVEL",   14, C.COR_HUD_LABEL, px+510, py+14)
        pygame.draw.line(surf, C.COR_HUD_BORDA, (px+16, py+36), (px+pw-16, py+36), 1)

        if not ranking:
            _texto(surf, "Nenhuma partida registrada ainda.", 18, C.COR_HUD_TEXTO, cx, py+56, centralizar=True)
        else:
            max_score = ranking[0]["pontuacao"] if ranking else 1
            for i, entrada in enumerate(ranking[:EXIBIR]):
                iy = py + 44 + i * 48
                if entrada.get("nome") == destaque_nome:
                    hl = pygame.Surface((pw-16, 42), pygame.SRCALPHA)
                    hl.fill((255, 220, 50, 18))
                    surf.blit(hl, (px+8, iy-2))
                if i < 3:
                    _texto(surf, _MEDALHAS[i], 18, _COR_MEDALHA[i], px+22, iy+4)
                else:
                    _texto(surf, str(i+1), 18, C.COR_HUD_LABEL, px+22, iy+4)
                cor_nome = C.AMARELO if entrada.get("nome") == destaque_nome else C.COR_HUD_TEXTO
                _texto(surf, entrada["nome"][:14], 18, cor_nome, px+70, iy+4)
                score = entrada["pontuacao"]
                prop = score / max(max_score, 1)
                bx2, by2, bw2, bh2 = px+390, iy+14, 100, 8
                pygame.draw.rect(surf, (20, 20, 30), (bx2, by2, bw2, bh2), border_radius=3)
                if prop > 0:
                    cor_barra = _COR_MEDALHA[i] if i < 3 else C.VERDE_UI
                    pygame.draw.rect(surf, cor_barra, (bx2, by2, int(bw2*prop), bh2), border_radius=3)
                _texto(surf, str(score), 18, C.COR_HUD_DESTAQUE, px+390, iy+4)
                _texto(surf, str(entrada.get("nivel", 1)), 18, C.COR_FRUTA_BOOST, px+510, iy+4)

        _texto(surf, "[ESC] Menu   [ENTER] Jogar", 14, C.COR_HUD_LABEL, cx, py+ph+16, centralizar=True)

        flip()
        clock.tick(C.FPS_BASE)
        frame += 1


def tela_pause(surf, clock, flip):
    _init_fonts()
    frame = 0
    cx = C.LARGURA_TELA // 2

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                return

        overlay = pygame.Surface((C.LARGURA_TELA, C.ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surf.blit(overlay, (0, 0))

        pw, ph = 380, 160
        _painel_vidro(surf, cx - pw//2, C.ALTURA//2 - ph//2, pw, ph, cor_borda=C.AMARELO)

        brilho = 0.8 + 0.2 * math.sin(frame * 0.08)
        cor_p = tuple(int(c * brilho) for c in C.AMARELO)
        _texto(surf, "II  PAUSADO", 48, cor_p, cx, C.ALTURA//2 - 44, centralizar=True)
        _texto(surf, "[P]  continuar", 18, C.COR_HUD_TEXTO, cx, C.ALTURA//2 + 28, centralizar=True)

        flip()
        clock.tick(15)
        frame += 1