# Breakout

> Sistema de colisão reflexiva com progressão destrutiva, implementado com física de reflexão angular e dificuldade escalável.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=flat-square)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=flat-square)

---

## Sumário

- [01 · Conceito Central](#01--conceito-central)
- [02 · Mecânicas Principais](#02--mecânicas-principais)
- [03 · Arquitetura e Módulos](#03--arquitetura-e-módulos)
- [04 · Decisões de Design](#04--decisões-de-design)
- [05 · Estrutura do Projeto](#05--estrutura-do-projeto)
- [06 · Controles](#06--controles)
- [07 · Instalação e Execução](#07--instalação-e-execução)

---

## 01 · Conceito Central

O Breakout Engine é projetado como um **sistema de colisão reflexiva com progressão destrutiva**, no qual o estado do jogo evolui por meio de regras físicas determinísticas e entradas do usuário interpretadas como intenções de posicionamento.

A bola não é controlada diretamente — o jogador posiciona o paddle e influencia a trajetória por meio do **ponto de impacto**, que determina o ângulo de reflexão. Cada tijolo destruído altera o estado do sistema e incrementa a velocidade, criando uma progressão contínua de dificuldade até a eliminação completa da grade.

---

## 02 · Mecânicas Principais

| Mecânica | Descrição |
|----------|-----------|
| **Reflexão Angular** | O ponto de impacto no paddle determina o ângulo de saída da bola (20° a 160°), dando controle real ao jogador. |
| **Colisão MTV** | Minimum Translation Vector aplicado na colisão bola-tijolo para reflexão correta por face, sem tunneling. |
| **Velocidade Progressiva** | Cada tijolo destruído incrementa levemente a velocidade da bola, com teto máximo definido. |
| **Grade de Tijolos** | Grade gerada dinamicamente com valores de pontuação distintos por linha. |
| **Vidas** | O jogador possui vidas limitadas. Perder a bola consome uma vida; ao esgotar todas, a sessão encerra. |
| **High Score** | Melhor pontuação persistida localmente entre sessões. |

---

## 03 · Arquitetura e Módulos

O sistema segue separação estrita de responsabilidades: `Application` não conhece regras de jogo; `GameSession` não conhece `pygame.display`.

| Módulo | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| **Config** | `core/config.py` | Constantes globais e paleta de cores. |
| **GameState** | `core/state.py` | Enum de estados da máquina de estados (menu, jogo, pausa, game over). |
| **InputHandler** | `core/input_handler.py` | Abstração de entrada: teclado e mouse. |
| **GameSession** | `core/game_session.py` | Lógica de jogo, física e detecção de colisões. |
| **Application** | `core/application.py` | Loop principal e orquestração da máquina de estados. |
| **Paddle** | `entities/paddle.py` | Modelagem do paddle: movimento e renderização. |
| **Ball** | `entities/ball.py` | Modelagem da bola: física e reflexão. |
| **Brick** | `entities/brick.py` | Modelagem do tijolo: pontuação e renderização. |
| **BrickGrid** | `entities/brick_grid.py` | Grade de tijolos e colisão MTV. |
| **HUD** | `ui/hud.py` | Interface: score, vidas e overlays de estado. |
| **ScoreIO** | `utils/score_io.py` | Persistência do high score em arquivo local. |

---

## 04 · Decisões de Design

- **Separação de responsabilidades** — `Application` orquestra estados sem conhecer regras de domínio; `GameSession` processa a lógica sem acoplamento à camada de apresentação.
- **Colisão MTV** — a resolução por Minimum Translation Vector garante reflexão precisa por face do tijolo, eliminando artefatos de tunneling comuns em implementações simples.
- **Reflexão angular no paddle** — inspirada no Breakout original: o ponto de impacto relativo ao centro do paddle determina o ângulo de saída (20° a 160°), transferindo controle tático ao jogador.
- **Velocidade progressiva** — a aceleração incremental por tijolo destruído mantém curva de dificuldade consistente com teto definido, evitando estados impossíveis.
- **Persistência leve** — high score armazenado em `~/.breakout_highscore`, sem dependências externas.

---

## 05 · Estrutura do Projeto

```
breakout/
├── main.py
├── core/
│   ├── config.py
│   ├── state.py
│   ├── input_handler.py
│   ├── game_session.py
│   └── application.py
├── entities/
│   ├── paddle.py
│   ├── ball.py
│   ├── brick.py
│   └── brick_grid.py
├── ui/
│   └── hud.py
└── utils/
    └── score_io.py
```

---

## 06 · Controles

| Tecla | Acao |
|-------|------|
| `Mouse` / `Seta Esquerda` / `Seta Direita` | Mover o paddle |
| `Espaco` | Lançar bola |
| `P` | Pausar / retomar |
| `ESC` | Sair do jogo |

---

## 07 · Instalação e Execução

**Requisitos:** Python 3.10 ou superior · Pygame

```bash
# Instalar dependências
pip install pygame

# Executar
python main.py
```

---

<p align="center">Breakout · Classic Games · Projeto de Portfolio · 2026</p>