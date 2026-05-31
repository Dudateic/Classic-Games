# Classic Games

> Coleção de sistemas interativos clássicos implementados como modelos computacionais determinísticos.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-latest-013243?style=flat-square&logo=numpy)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=flat-square)
![License](https://img.shields.io/badge/licença-Open%20Source-brightgreen?style=flat-square)

---

## Sumário

- [01 · Visão Geral](#01--visão-geral)
- [02 · Jogos Incluídos](#02--jogos-incluídos)
- [03 · Princípio Unificador](#03--princípio-unificador)
- [04 · Arquitetura Conceitual](#04--arquitetura-conceitual)
- [05 · Estrutura do Projeto](#05--estrutura-do-projeto)
- [06 · Roadmap](#06--roadmap)
- [07 · Como Executar](#07--como-executar)

---

## 01 · Visão Geral

Este repositório reúne implementações digitais de jogos clássicos organizados como **sistemas interativos independentes**, concebidos sob um conjunto unificado de princípios de modelagem computacional.

Cada jogo representa uma instância de um **sistema dinâmico discreto**, no qual interação humana, regras formais e evolução temporal se combinam para produzir comportamento emergente consistente e reprodutível.

Mais do que uma coleção de jogos, este projeto constitui um **laboratório de sistemas interativos baseados em regras**, voltado ao estudo de simulação, controle e feedback em ambientes computacionais.

---

## 02 · Jogos Incluídos

| Jogo | Descrição | Mecânicas |
|------|-----------|-----------|
| **Tetris** | Sistema de organização espacial sob restrição, baseado em encaixe e otimização de espaço em tempo real. | Gravidade · Encaixe |
| **Snake** | Sistema de crescimento incremental em ambiente contínuo limitado com controle direcional progressivo. | Crescimento · Colisão |
| **Breakout** | Sistema de colisão reflexiva com progressão destrutiva. Física determinística de bola e raquete. | Física · Reflexão |
| **Space Invaders** | Sistema de padrões de movimento e resposta defensiva progressiva. Ondas de inimigos com dificuldade escalável. | Padrões · Resposta |

---

## 03 · Princípio Unificador

Todos os sistemas seguem quatro pilares conceituais:

- **Interação** — Interpretação de intenções humanas, não manipulação direta de estado.
- **Estado** — Representação completa e consistente do mundo interno a cada instante.
- **Evolução** — Atualização discreta baseada em ciclos sucessivos de simulação.
- **Representação** — Saída visual como projeção do estado interno, sem influência na lógica.

---

## 04 · Arquitetura Conceitual

Todos os jogos seguem a mesma **separação conceitual de responsabilidades** e o mesmo fluxo de execução:

```
Entrada --> Interpretação --> Validação --> Simulação --> Atualização --> Renderização
```

| Módulo | Responsabilidade |
|--------|-----------------|
| Lógica de Regras | Núcleo do tabuleiro e física |
| Sistema de Entrada | Captura e interpretação de input |
| Sistema de Simulação | Loop principal, evolução de estado |
| Renderização | Projeção visual do estado |
| Efeitos e Feedback | Partículas, flash, shake |
| Pontuação e Persistência | Score, níveis, leaderboard |

---

## 05 · Estrutura Geral do Projeto

```
Games_Classic/
├── Breakout/
├── Snake/
├── Space Invaders/
├── Tetris/
└── Readme/
```

---

## 06 · Roadmap

- [ ] Tetris — implementação completa
- [ ] Snake — implementação completa
- [ ] Breakout — implementação completa
- [ ] Space Invaders — implementação completa
- [ ] Pong — em desenvolvimento
- [ ] Flappy Bird — em desenvolvimento
- [ ] Minesweeper  — em desenvolvimento
- [ ] Simon Says — em desenvolvimento
- [ ] Asteroids — em desenvolvimento
- [ ] Frogger  — em desenvolvimento
- [ ] Pac-Man — em desenvolvimento
- [ ] Galaga — em desenvolvimento
- [ ] Platformer — em desenvolvimento
- [ ] Puzzle Bobble — em desenvolvimento
- [ ] Roguelike — em desenvolvimento
- [ ] Engine compartilhada entre jogos

---

## 07 · Como Executar

**Requisitos:** Python 3.10 ou superior · Pygame 2.x · NumPy

```bash
# Instalar dependências
pip install pygame numpy

# Entrar no diretório do jogo
cd Tetris

# Executar
python main.py
```

---

<p align="center">Classic Games · Projeto de Portfolio · 2025</p>
