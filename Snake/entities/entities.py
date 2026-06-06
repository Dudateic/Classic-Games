from __future__ import annotations
import random
import math
from dataclasses import dataclass, field
from typing import Literal
import pygame
import config.config as C

FruitType = Literal["bom", "ruim", "boost", "ouro"]
Direcao   = Literal["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]

OPOSTOS = {"CIMA": "BAIXO", "BAIXO": "CIMA", "ESQUERDA": "DIREITA", "DIREITA": "ESQUERDA"}
DELTA   = {"CIMA": (0, -1), "BAIXO": (0, 1), "ESQUERDA": (-1, 0), "DIREITA": (1, 0)}

COLS = C.LARGURA_JOGO  // C.TAMANHO_CELULA
ROWS = C.ALTURA        // C.TAMANHO_CELULA

class Cobra:
    def __init__(self) -> None:
        cx = (COLS // 2) * C.TAMANHO_CELULA
        cy = (ROWS // 2) * C.TAMANHO_CELULA
        self.corpo: list[tuple[int, int]] = [(cx, cy)]
        self.direcao: Direcao = "DIREITA"
        self._proxima_direcao: Direcao = "DIREITA"
        self.crescimento: int = 2
        self.viva: bool = True

    def definir_direcao(self, nova: Direcao) -> None:
        if nova != OPOSTOS[self.direcao]:
            self._proxima_direcao = nova

    def mover(self) -> None:
        self.direcao = self._proxima_direcao
        dx, dy = DELTA[self.direcao]
        hx, hy = self.corpo[0]
        nx = (hx + dx * C.TAMANHO_CELULA) % C.LARGURA_JOGO
        ny = (hy + dy * C.TAMANHO_CELULA) % C.ALTURA
        nova_cabeca = (nx, ny)

        # Se não está crescendo, a cauda vai sair nesse passo,
        # então não conta como obstáculo na detecção de colisão.
        corpo_colisao = self.corpo if self.crescimento > 0 else self.corpo[:-1]
        if nova_cabeca in corpo_colisao:
            self.viva = False
            return

        self.corpo.insert(0, nova_cabeca)
        if self.crescimento > 0:
            self.crescimento -= 1
        else:
            self.corpo.pop()

    def crescer(self, n: int) -> None:
        self.crescimento += n

    def encolher(self, n: int) -> None:
        for _ in range(n):
            if len(self.corpo) > 1:
                self.corpo.pop()

    @property
    def cabeca(self) -> tuple[int, int]:
        return self.corpo[0]

    def __len__(self) -> int:
        return len(self.corpo)


@dataclass
class Fruta:
    tipo: FruitType
    pos:  tuple[int, int]
    cor:  tuple[int, int, int]
    pulso: float = 0.0

    def atualizar(self) -> None:
        self.pulso += 0.12

    def raio_pulso(self) -> float:
        return 2.5 + 1.5 * math.sin(self.pulso)


def gerar_fruta(tipo: FruitType, cobra: Cobra, frutas: list[Fruta]) -> Fruta:
    posicoes_ocupadas = set(cobra.corpo) | {f.pos for f in frutas}
    while True:
        x = random.randint(0, COLS - 1) * C.TAMANHO_CELULA
        y = random.randint(0, ROWS - 1) * C.TAMANHO_CELULA
        if (x, y) not in posicoes_ocupadas:
            cor = _cor_fruta(tipo)
            return Fruta(tipo=tipo, pos=(x, y), cor=cor)


def _cor_fruta(tipo: FruitType) -> tuple[int, int, int]:
    if tipo == "bom":
        return random.choice(C.COR_FRUTA_BOA)
    if tipo == "ruim":
        return C.COR_FRUTA_RUIM
    if tipo == "boost":
        return C.COR_FRUTA_BOOST
    return C.COR_FRUTA_OURO


@dataclass
class Particula:
    x:      float
    y:      float
    vx:     float
    vy:     float
    cor:    tuple[int, int, int]
    vida:   int = C.PARTICULA_VIDA
    vida_max: int = C.PARTICULA_VIDA

    def atualizar(self) -> None:
        self.x   += self.vx
        self.y   += self.vy
        self.vy  += 0.15
        self.vx  *= 0.96
        self.vida -= 1

    @property
    def ativo(self) -> bool:
        return self.vida > 0

    @property
    def alpha(self) -> int:
        return int(255 * (self.vida / self.vida_max))

    @property
    def raio(self) -> float:
        return max(1.0, 4.0 * (self.vida / self.vida_max))


def criar_particulas(pos: tuple[int, int], cores: list, n: int = C.PARTICULAS_POR_FRUTA) -> list[Particula]:
    cx = pos[0] + C.TAMANHO_CELULA / 2
    cy = pos[1] + C.TAMANHO_CELULA / 2
    particulas = []
    for _ in range(n):
        angulo = random.uniform(0, 2 * math.pi)
        vel    = random.uniform(1.5, 4.5)
        cor    = random.choice(cores)
        particulas.append(Particula(
            x=cx, y=cy,
            vx=math.cos(angulo) * vel,
            vy=math.sin(angulo) * vel - random.uniform(0, 2),
            cor=cor,
        ))
    return particulas