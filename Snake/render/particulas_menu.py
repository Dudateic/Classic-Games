from __future__ import annotations
import math
import random
import pygame
import config.config as C


class _Particula:
    __slots__ = ("x", "y", "vx", "vy", "cor", "raio", "alpha", "vida", "vida_max")

    def __init__(self) -> None:
        self.x        = random.uniform(0, C.LARGURA_TELA)
        self.y        = random.uniform(0, C.ALTURA)
        angulo        = random.uniform(0, math.pi * 2)
        spd           = random.uniform(0.2, 0.7)
        self.vx       = math.cos(angulo) * spd
        self.vy       = math.sin(angulo) * spd
        self.raio     = random.uniform(1.5, 3.5)
        self.cor      = random.choice(C.ARCO_IRIS_NEON)
        self.vida_max = random.randint(180, 360)
        self.vida     = self.vida_max
        self.alpha    = 0

    def atualizar(self) -> None:
        self.x = (self.x + self.vx) % C.LARGURA_TELA
        self.y = (self.y + self.vy) % C.ALTURA
        self.vida -= 1
        fade_in    = min(1.0, (self.vida_max - self.vida) / 30)
        fade_out   = min(1.0, self.vida / 30)
        self.alpha = int(180 * min(fade_in, fade_out))

    @property
    def ativo(self) -> bool:
        return self.vida > 0


_pool: list[_Particula] = []
_QUANTIDADE = 10


def resetar() -> None:
    global _pool
    _pool = []


def atualizar() -> None:
    """Atualiza e reabastece o pool."""
    global _pool
    _pool = [p for p in _pool if p.ativo]
    while len(_pool) < _QUANTIDADE:
        _pool.append(_Particula())
    for p in _pool:
        p.atualizar()


def desenhar(surf: pygame.Surface) -> None:
    """Renderiza todas as particulas do pool."""
    for p in _pool:
        r = int(p.raio)
        if r < 1:
            continue
        s = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*p.cor, p.alpha), (r + 1, r + 1), r)
        surf.blit(s, (int(p.x) - r - 1, int(p.y) - r - 1))