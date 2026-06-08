from __future__ import annotations
import math
import random
import pygame
import config.config as C
import render.texto as Texto
from render.fundo import grade_simples

class _Confete:
    """Partícula colorida que cai em espiral para o efeito de comemoração."""

    CORES = [
        (255, 215,   0),
        (255,  80,  80),
        (80,  200, 255),
        (180, 255, 100),
        (255, 160,  40),
        (220, 120, 255),
    ]

    def __init__(self, cx: int, largura: int, altura: int) -> None:
        self.x = cx + random.uniform(-largura * 0.4, largura * 0.4)
        self.y = random.uniform(-altura * 0.3, 0)
        self.vy = random.uniform(1.5, 4.5)
        self.vx = random.uniform(-1.5, 1.5)
        self.cor = random.choice(self.CORES)
        self.w = random.randint(6, 14)
        self.h = random.randint(4, 8)
        self.angulo = random.uniform(0, 360)
        self.spin = random.uniform(-5, 5)
        self.alpha = 255
        self.fade = random.uniform(1.2, 2.8)
        self._altura = altura

    @property
    def vivo(self) -> bool:
        return self.alpha > 0 and self.y < self._altura + 20

    def atualizar(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.angulo += self.spin
        self.alpha = max(0, self.alpha - self.fade)

    def desenhar(self, surf: pygame.Surface) -> None:
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        s.fill((*self.cor, int(self.alpha)))
        rs = pygame.transform.rotate(s, self.angulo)
        surf.blit(rs, rs.get_rect(center=(int(self.x), int(self.y))))


class TelaNovoRecorde:
    """
    Exibida quando o jogador bate o recorde.

    Retorna: 'JOGAR' | 'RANKING' | 'MENU'
    """

    _INTERVALO_CONFETE = 3
    _MAX_CONFETES = 120

    def __init__(self, fontes, particulas) -> None:
        self._pt = particulas
        self._confetes: list[_Confete] = []
        self._frame_confete = 0

    def executar(
        self,
        surf: pygame.Surface,
        clock: pygame.time.Clock,
        flip,
        pontuacao: int,
        highscore_anterior: int,
        nivel: int,
        nome_jogador: str = "",
    ) -> str:

        W, H = surf.get_size()
        cx = W // 2

        opcoes   = ["JOGAR NOVAMENTE", "VER RANKING", "MENU PRINCIPAL"]
        retornos = ["JOGAR", "RANKING", "MENU"]
        selecionado = 0
        frame = 0

        self._confetes.clear()
        self._frame_confete = 0

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

            self._frame_confete += 1
            if (
                self._frame_confete % self._INTERVALO_CONFETE == 0
                and len(self._confetes) < self._MAX_CONFETES
            ):
                self._confetes.append(_Confete(cx, W, H))

            for c in self._confetes:
                c.atualizar()
                c.desenhar(surf)
            self._confetes = [c for c in self._confetes if c.vivo]

            pulso = math.sin(frame * 0.07) * 0.5 + 0.5   # 0..1
            halo_r = int(190 + pulso * 30)
            halo_surf = pygame.Surface((halo_r * 2, halo_r * 2), pygame.SRCALPHA)

            surf.blit(halo_surf, (cx - halo_r, 80 - halo_r))

            self._desenhar_estrelas(surf, cx, 80, frame)

            escala = 1.0 + 0.04 * math.sin(frame * 0.1)
            titulo_cor = self._cor_arco_iris(frame)
            Texto.desenhar(
                surf, "NOVO RECORDE!", 200,
                titulo_cor, cx, 150, centralizar=True,
            )

            Texto.desenhar(
                surf, str(pontuacao), 80, C.AMARELO,
                cx, 250, centralizar=True,
            )

            py_menu = 380
            for i, op in enumerate(opcoes):
                iy = py_menu + i * 52
                if i == selecionado:
                    Texto.desenhar(surf, f"[ {op} ]", 26.5, C.AMARELO, cx, iy, centralizar=True)
                else:
                    Texto.desenhar(surf, op, 26.5, C.COR_HUD_TEXTO, cx, iy, centralizar=True)

            flip()
            clock.tick(C.FPS_BASE)
            frame += 1

    @staticmethod
    def _cor_arco_iris(frame: int) -> tuple[int, int, int]:
        t = frame * 0.04
        r = int((math.sin(t + 0.0) * 0.5 + 0.5) * 200 + 55)
        g = int((math.sin(t + 2.1) * 0.5 + 0.5) * 200 + 55)
        b = int((math.sin(t + 4.2) * 0.5 + 0.5) * 180 + 55)
        return (r, g, b)

    @staticmethod
    def _desenhar_estrelas(
        surf: pygame.Surface, cx: int, cy: int, frame: int
    ) -> None:
        """Desenha 6 estrelas orbitando o título."""
        raio_orbit = 155
        n = 6
        for k in range(n):
            ang = frame * 0.018 + k * (2 * math.pi / n)
            sx = cx + int(math.cos(ang) * raio_orbit)
            sy = cy + int(math.sin(ang) * raio_orbit * 0.35)
            brilho = int(180 + 75 * math.sin(frame * 0.12 + k))
            cor = (brilho, brilho, 60)
            tamanho = 5 + int(3 * math.sin(frame * 0.09 + k * 1.3))
            _desenhar_estrela_pixel(surf, sx, sy, tamanho, cor)


def _desenhar_estrela_pixel(
    surf: pygame.Surface,
    x: int, y: int,
    tamanho: int,
    cor: tuple[int, int, int],
) -> None:

    pygame.draw.line(surf, cor, (x - tamanho, y), (x + tamanho, y), 2)
    pygame.draw.line(surf, cor, (x, y - tamanho), (x, y + tamanho), 2)
    d = max(1, tamanho // 2)
    pygame.draw.line(surf, cor, (x - d, y - d), (x + d, y + d), 1)
    pygame.draw.line(surf, cor, (x + d, y - d), (x - d, y + d), 1)