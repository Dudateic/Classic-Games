from __future__ import annotations
import time
import random
import os
import json
import config.config as C
from entities.entities import Cobra, Fruta, Particula, gerar_fruta, criar_particulas


def carregar_highscore() -> int:
    ranking = carregar_ranking()
    if ranking:
        return ranking[0]["pontuacao"]
    return 0


def carregar_ranking() -> list[dict]:
    """Lê ranking.json e retorna lista ordenada por pontuação."""
    if os.path.exists(C.ARQUIVO_RANKING):
        try:
            with open(C.ARQUIVO_RANKING, "r", encoding="utf-8") as f:
                dados = json.load(f)
            if isinstance(dados, list):
                return dados
        except (ValueError, IOError, json.JSONDecodeError):
            pass
    return []


def salvar_entrada_ranking(nome: str, pontuacao: int, nivel: int) -> list[dict]:
    """Adiciona entrada ao ranking, mantém top-20, retorna ranking atualizado."""
    ranking = carregar_ranking()
    entrada = {"nome": nome, "pontuacao": pontuacao, "nivel": nivel}
    ranking.append(entrada)
    ranking.sort(key=lambda x: x["pontuacao"], reverse=True)
    ranking = ranking[:20]
    try:
        with open(C.ARQUIVO_RANKING, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)
    except IOError:
        pass
    return ranking

class EstadoJogo:
    def __init__(self) -> None:
        self.cobra      = Cobra()
        self.frutas:     list[Fruta]    = []
        self.particulas: list[Particula] = []

        self.pontuacao  = 0
        self.nivel      = 1
        self.highscore  = carregar_highscore()

        self.boost_ativo        = False
        self.boost_tempo_inicio = 0.0
        self.boost_restante     = 0.0
        self.fruta_ouro_presente = False

        self._ticks_passo = C.TICKS_POR_PASSO_BASE
        self._tick_atual  = 0

        self.mensagem_texto = ""
        self.mensagem_timer = 0
        self.mensagem_cor   = C.VERDE_UI

        self._popular_frutas()

    def _popular_frutas(self) -> None:
        for _ in range(C.QTD_FRUTAS_BOAS):
            self.frutas.append(gerar_fruta("bom",   self.cobra, self.frutas))
        for _ in range(C.QTD_FRUTAS_RUINS):
            self.frutas.append(gerar_fruta("ruim",  self.cobra, self.frutas))
        for _ in range(C.QTD_FRUTAS_BOOST):
            self.frutas.append(gerar_fruta("boost", self.cobra, self.frutas))

    def tick(self) -> None:
        if not self.cobra.viva:
            return

        self._atualizar_particulas()
        self._atualizar_frutas()
        self._atualizar_boost()
        self._atualizar_mensagem()
        self._tentar_spawn_fruta_ouro()
        self._avancar_passo()
        self._verificar_highscore()

    def _atualizar_particulas(self) -> None:
        self.particulas = [p for p in self.particulas if p.ativo]
        for p in self.particulas:
            p.atualizar()

    def _atualizar_frutas(self) -> None:
        for f in self.frutas:
            f.atualizar()

    def _atualizar_boost(self) -> None:
        if self.boost_ativo:
            elapsed = time.time() - self.boost_tempo_inicio
            self.boost_restante = max(0.0, C.DURACAO_BOOST - elapsed)
            if elapsed >= C.DURACAO_BOOST:
                self.boost_ativo    = False
                self.boost_restante = 0.0

    def _atualizar_mensagem(self) -> None:
        if self.mensagem_timer > 0:
            self.mensagem_timer -= 1

    def _tentar_spawn_fruta_ouro(self) -> None:
        if not self.fruta_ouro_presente:
            if random.random() < C.CHANCE_FRUTA_OURO / C.FPS_BASE:
                self.frutas.append(gerar_fruta("ouro", self.cobra, self.frutas))
                self.fruta_ouro_presente = True

    def _avancar_passo(self) -> None:
        self._tick_atual += 1
        passo = max(
            C.TICKS_POR_PASSO_MIN,
            self._ticks_passo - (C.FPS_BOOST_REDUCAO if self.boost_ativo else 0),
        )
        if self._tick_atual >= passo:
            self._tick_atual = 0
            self.cobra.mover()
            if self.cobra.viva:
                self._verificar_colisao_frutas()

    def _verificar_highscore(self) -> None:
        if self.pontuacao > self.highscore:
            self.highscore = self.pontuacao

    def _verificar_colisao_frutas(self) -> None:
        cabeca    = self.cobra.cabeca
        corpo_set = set(self.cobra.corpo)
        novas, coletadas, recolocar = [], [], []

        for f in self.frutas:
            if f.pos == cabeca:
                coletadas.append(f)
            elif f.pos in corpo_set:
                recolocar.append(f.tipo)
            else:
                novas.append(f)

        self.frutas = novas
        for tipo in recolocar:
            self.frutas.append(gerar_fruta(tipo, self.cobra, self.frutas))
        for f in coletadas:
            self._processar_coleta(f)

    def _pontuacao_por_fruta(self, cor: tuple[int, int, int]):
        match cor:
            case C.VERDE:
                return 1
            case C.LARANJA:
                return 2
            case C.CIANO:
                return 3
            case C.BRANCO:
                return 4
            case C.AMARELO:
                return 5
        print(cor, C.CIANO)

        return 0

    
    def _processar_coleta(self, fruta: Fruta) -> None:
        t, cor, pos = fruta.tipo, fruta.cor, fruta.pos

        if t == "bom":
            self.pontuacao += self._pontuacao_por_fruta(cor)
            self.cobra.crescer(2)
            self.particulas += criar_particulas(pos, C.COR_PARTICULA_BOA)
            self.frutas.append(gerar_fruta("bom", self.cobra, self.frutas))
            self._msg(f"{self._pontuacao_por_fruta(cor)}", C.VERDE_UI)

        elif t == "ruim":
            self.pontuacao = max(0, self.pontuacao - 1)
            self.cobra.encolher(3)
            self.particulas += criar_particulas(pos, C.COR_PARTICULA_RUIM)
            self.frutas.append(gerar_fruta("ruim", self.cobra, self.frutas))
            self._msg("-1", C.VERMELHO)

        elif t == "boost":
            self.boost_ativo        = True
            self.boost_tempo_inicio = time.time()
            self.boost_restante     = C.DURACAO_BOOST
            self.particulas += criar_particulas(pos, C.COR_PARTICULA_BOOST, n=16)
            self.frutas.append(gerar_fruta("boost", self.cobra, self.frutas))
            self._msg("BOOST!", C.COR_FRUTA_BOOST)

        elif t == "ouro":
            self.pontuacao += 5
            self.cobra.crescer(3)
            self.particulas += criar_particulas(pos, C.COR_PARTICULA_OURO, n=20)
            self.fruta_ouro_presente = False
            self._msg("+5", C.COR_FRUTA_OURO)

        self._verificar_nivel()

    def _verificar_nivel(self) -> None:
        novo = min(C.NIVEL_MAX, 1 + self.pontuacao // C.PONTOS_POR_NIVEL)
        if novo > self.nivel:
            self.nivel = novo
            self._ticks_passo = max(
                C.TICKS_POR_PASSO_MIN,
                C.TICKS_POR_PASSO_BASE - (self.nivel - 1),
            )
            self._msg(f"NIVEL {self.nivel}!", C.AMARELO)

    def _msg(self, texto: str, cor: tuple) -> None:
        self.mensagem_texto = texto
        self.mensagem_timer = 90
        self.mensagem_cor   = cor

    def reiniciar(self) -> None:
        hs = self.highscore
        self.__init__()
        self.highscore = max(hs, carregar_highscore())