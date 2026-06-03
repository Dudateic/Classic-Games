# Breakout — Edição Expandida

> Sistema de colisão reflexiva com progressão por níveis, loja de upgrades, sistema de partículas e ranking local. Implementado com física de reflexão angular, colisão MTV e dificuldade escalável.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-CE%202.x-00B140?style=flat-square)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=flat-square)

---

## Sumário

- [01 · Conceito Central](#01--conceito-central)
- [02 · Mecânicas Principais](#02--mecânicas-principais)
- [03 · Arquitetura e Módulos](#03--arquitetura-e-módulos)
- [04 · Decisões de Design](#04--decisões-de-design)
- [05 · Estrutura do Projeto](#05--estrutura-do-projeto)
- [06 · Controles](#07--controles)
- [07 · Upgrades Disponíveis](#08--upgrades-disponíveis)
- [08 · Níveis](#09--níveis)
- [09 · Instalação e Execução](#10--instalação-e-execução)

---

## 01 · Conceito Central

O Breakout Engine é projetado como um **sistema de colisão reflexiva com progressão destrutiva**, no qual o estado do jogo evolui por meio de regras físicas determinísticas e entradas do usuário interpretadas como intenções de posicionamento.

A bola não é controlada diretamente — o jogador posiciona o paddle e influencia a trajetória por meio do **ponto de impacto**, que determina o ângulo de reflexão. Cada tijolo destruído altera o estado do sistema e incrementa a velocidade, criando uma progressão contínua de dificuldade.

A progressão se dá em **níveis distintos**, cada qual com layout próprio. Entre níveis, o jogador pode investir pontos em upgrades permanentes por sessão. Ao zerar todos os níveis, a tela de créditos é exibida com scroll animado.

---

## 02 · Mecânicas Principais

| Mecânica | Descrição |
|----------|-----------|
| **Reflexão Angular** | O ponto de impacto no paddle determina o ângulo de saída da bola (20° a 160°), dando controle real ao jogador. |
| **Colisão MTV** | Minimum Translation Vector aplicado na colisão bola-tijolo para reflexão correta por face, sem tunneling. |
| **Velocidade Progressiva** | Cada tijolo destruído incrementa levemente a velocidade da bola, com teto máximo definido. |
| **Tijolos Resistentes** | Tijolos com HP 2 ou 3 ficam progressivamente mais escuros e exibem o HP restante. |
| **Grade de Tijolos** | Grade gerada por layouts pré-definidos (5 layouts únicos) ou proceduralmente para níveis além do 5°. |
| **Loja de Upgrades** | Entre níveis, o jogador gasta pontos em melhorias permanentes para a sessão. |
| **Sistema de Partículas** | Destruição de tijolos gera partículas visuais. |
| **Vidas** | O jogador possui vidas limitadas. Perder a bola consome uma vida; ao esgotar todas, a sessão encerra. |
| **High Score (Top 5)** | Ranking dos 5 melhores resultados persistidos localmente em JSON. |

---

## 03 · Arquitetura e Módulos

O sistema segue separação estrita de responsabilidades: `Application` não conhece regras de jogo; `GameSession` não conhece `pygame.display`; cada tela é um módulo independente.

| Módulo | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| **Config** | `core/config.py` | Constantes globais, paleta de cores e definição de upgrades. |
| **GameState** | `core/state.py` | Enum com os 12 estados da máquina de estados. |
| **InputHandler** | `core/input_handler.py` | Abstração de entrada: teclado e mouse. |
| **GameSession** | `core/game_session.py` | Lógica de jogo, física, colisões e integração com partículas. |
| **Application** | `core/application.py` | Loop principal e orquestração da máquina de estados. |
| **Paddle** | `entities/paddle.py` | Modelagem do paddle: movimento e renderização. |
| **Ball** | `entities/ball.py` | Modelagem da bola: física e reflexão. |
| **Brick** | `entities/brick.py` | Modelagem do tijolo: HP múltiplo, pontuação e renderização. |
| **BrickGrid** | `entities/brick_grid.py` | Grade de tijolos e colisão MTV. |
| **Particles** | `systems/particles.py` | Sistema de partículas para destruição de tijolos. |
| **LevelLoader** | `levels/level_loader.py` | Layouts de nível (pirâmide, colunas, X, grade, etc.) e geração procedural. |
| **HUD** | `ui/hud.py` | Interface: score, vidas, nível atual e overlays de estado. |
| **SplashScreen** | `ui/screens/splash_screen.py` | Tela de abertura do estúdio (2,5 s). |
| **ReadyScreen** | `ui/screens/ready_screen.py` | Contagem regressiva 3-2-1 antes de cada nível. |
| **LevelCompletedScreen** | `ui/screens/level_completed_screen.py` | Estatísticas e bônus ao limpar um nível. |
| **UpgradeScreen** | `ui/screens/upgrade_screen.py` | Loja de upgrades entre níveis. |
| **SettingsScreen** | `ui/screens/settings_screen.py` | Configurações: mouse, volume e tela cheia. |
| **HighScoresScreen** | `ui/screens/high_scores_screen.py` | Ranking Top 5 local. |
| **CreditsScreen** | `ui/screens/credits_screen.py` | Créditos animados com scroll ao zerar o jogo. |
| **ScoreIO** | `utils/score_io.py` | Persistência do Top 5 em JSON local (`~/.breakout_scores`). |

---

## 04 · Decisões de Design

- **Separação de responsabilidades** — `Application` orquestra estados sem conhecer regras de domínio; `GameSession` processa a lógica sem acoplamento à camada de apresentação; cada tela vive em seu próprio módulo.
- **Colisão MTV** — a resolução por Minimum Translation Vector garante reflexão precisa por face do tijolo, eliminando artefatos de tunneling comuns em implementações simples.
- **Reflexão angular no paddle** — inspirada no Breakout original: o ponto de impacto relativo ao centro do paddle determina o ângulo de saída (20° a 160°), transferindo controle tático ao jogador.
- **Velocidade progressiva** — a aceleração incremental por tijolo destruído mantém curva de dificuldade consistente com teto definido, evitando estados impossíveis.
- **Tijolos com HP múltiplo** — tijolos resistentes adicionam profundidade tática sem complicar a física; a representação visual degradada dá feedback imediato ao jogador.
- **Loja de upgrades** — o gasto voluntário de pontos cria dilema estratégico e estende a curva de progressão além do aumento de velocidade.
- **Geração procedural a partir do nível 6** — seed baseada no número do nível garante reprodutibilidade sem necessidade de layouts manuais adicionais.
- **Persistência leve** — Top 5 armazenado em `~/.breakout_scores` como JSON, sem dependências externas.

---

## 05 · Estrutura do Projeto

```
breakout/
├── main.py
├── core/
│   ├── application.py
│   ├── config.py
│   ├── state.py
│   ├── input_handler.py
│   └── game_session.py
├── entities/
│   ├── paddle.py
│   ├── ball.py
│   ├── brick.py
│   └── brick_grid.py
├── systems/
│   └── particles.py
├── levels/
│   └── level_loader.py
├── ui/
│   ├── hud.py
│   └── screens/
│       ├── splash_screen.py
│       ├── ready_screen.py
│       ├── level_completed_screen.py
│       ├── upgrade_screen.py
│       ├── settings_screen.py
│       ├── high_scores_screen.py
│       └── credits_screen.py
└── utils/
    └── score_io.py
```

---

## 06 · Controles

| Tecla / Ação | Efeito |
|---|---|
| `Mouse` / `← →` | Move a raquete |
| `Espaço` | Lança a bola / confirma telas |
| `P` | Pausa / continua |
| `ESC` | Pausa → Menu → Sair |
| `H` | Abre o Ranking (Top 5) |
| `S` | Abre Configurações |
| `↑ ↓` (upgrades) | Seleciona item |
| `Enter` / `Z` (upgrades) | Compra o upgrade selecionado |

---

## 07 · Upgrades Disponíveis

| Upgrade | Custo | Efeito |
|---|---|---|
| Raquete Larga | 200 pts | +40 px na largura (por compra) |
| Bola Lenta | 150 pts | Velocidade máxima −20% |
| Vida Extra | 300 pts | +1 vida (máx. 5) |
| Boost de Pontos | 250 pts | ×2 pontos no nível seguinte |

---

## 08 · Níveis

- **5 layouts** únicos pré-definidos: Grade Clássica, Pirâmide, Colunas, X e Grade com tijolos duplos/triplos.
- A partir do nível 6, **geração procedural** com seed baseada no número do nível, garantindo reprodutibilidade.
- Tijolos com **HP 2–3** ficam progressivamente mais escuros e exibem o HP restante.

---

## 09 · Instalação e Execução

**Requisitos:** Python 3.10 ou superior · pygame-ce (ou pygame)

```bash
# Instalar dependências
pip install pygame-ce   # alternativa: pip install pygame

# Executar
python main.py
```

---

<p align="center">Breakout · Classic Games · Projeto de Portfolio · 2026</p>