# Galaxy Defense
> Sistema de simulação de combate espacial com progressão por ondas, máquina de estados e comportamento de inimigos baseado em Strategy Pattern.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
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

Galaxy Defense é um **sistema de simulação de combate espacial** no qual o jogador controla uma unidade contra ondas progressivas de inimigos gerados dinamicamente. O fluxo da aplicação é controlado por uma **máquina de estados finitos (FSM)**, responsável por isolar os diferentes contextos de execução e tornar o comportamento do sistema previsível e extensível.

O projeto demonstra construção de aplicação interativa com separação clara de responsabilidades, alta coesão e baixo acoplamento — permitindo evolução contínua sem impacto significativo nos módulos existentes.

---

## 02 · Mecânicas Principais

| Mecânica | Descrição |
|----------|-----------|
| **Ondas de Inimigos** | Inimigos gerados dinamicamente com padrões de movimentação distintos por fase. |
| **Strategy Pattern** | Comportamento de movimentação implementado como estratégias intercambiáveis: linear, senoidal e boss. |
| **Entidades de Elite** | Bosses com padrões compostos de alta resistência introduzidos progressivamente. |
| **Gerenciador de Fases** | Ajusta dinamicamente taxa de spawn, HP e complexidade comportamental ao longo da sessão. |
| **High Score (Top 10)** | Ranking dos 10 melhores resultados persistidos localmente em JSON. |

---

## 03 · Arquitetura e Módulos

O sistema segue separação estrita de responsabilidades: a FSM orquestra contextos sem conhecer regras de domínio; as entidades não conhecem a camada de apresentação; cada estratégia de movimentação vive em seu próprio módulo.

| Módulo | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| **FSM** | `core/fsm.py` | Máquina de estados: controle de transições entre menu, name entry, gameplay e leaderboard. |
| **SpawnManager** | `core/spawn_manager.py` | Geração dinâmica de inimigos com base na fase atual. |
| **PhaseManager** | `core/phase_manager.py` | Progressão de dificuldade: spawn rate, HP e padrões por fase. |
| **CollisionSystem** | `core/collision.py` | Detecção e resolução de colisões entre entidades. |
| **Player** | `entities/player.py` | Modelagem da unidade do jogador: movimento, disparo e renderização. |
| **Enemy** | `entities/enemy.py` | Modelagem das entidades inimigas: HP, pontuação e integração com strategies. |
| **Projectile** | `entities/projectile.py` | Modelagem dos projéteis: trajetória e ciclo de vida. |
| **LinearStrategy** | `strategies/linear.py` | Trajetória constante sem desvio. |
| **SinusoidalStrategy** | `strategies/sinusoidal.py` | Movimentação baseada em funções trigonométricas. |
| **BossStrategy** | `strategies/boss.py` | Padrões compostos de alta complexidade e resistência. |
| **HUD** | `ui/hud.py` | Interface: score, vidas, fase atual e overlays de estado. |
| **MenuScreen** | `ui/screens/menu_screen.py` | Tela de menu principal. |
| **NameEntryScreen** | `ui/screens/name_entry_screen.py` | Entrada do nome do jogador antes da sessão. |
| **LeaderboardScreen** | `ui/screens/leaderboard_screen.py` | Ranking Top 10 local. |
| **ScoreIO** | `data/score_io.py` | Persistência do Top 10 em JSON local. |

---

## 04 · Decisões de Design

- **Máquina de estados (FSM)** — isola completamente os contextos de execução, reduzindo o acoplamento entre interface e lógica de domínio e tornando o fluxo previsível e extensível.
- **Strategy Pattern** — o comportamento de movimentação dos inimigos é substituível em tempo de execução, eliminando lógica condicional acoplada e permitindo a introdução de novos padrões sem modificação das entidades base.
- **Gerenciador de fases** — centraliza o controle de dificuldade em um único módulo, garantindo curva de progressão consistente e evitando parâmetros espalhados pelo código.
- **Separação de responsabilidades** — `core` não conhece renderização; `ui` não conhece regras de domínio; `strategies` não conhecem entidades, cada módulo evolui de forma independente.
- **Persistência leve** — Top 10 armazenado localmente em JSON, sem dependências externas, com timestamp para identificação da sessão.

---

## 05 · Estrutura do Projeto
```
galaxy_defense/
├── assets
│   ├── sounds
│   │   ├── explosion.wav
│   │   ├── music.mp3
│   │   └── shoot.wav
│   └── sprites
│       ├── background.png
│       ├── player.png
│       ├── stormtrooper.png
│       ├── tie.png
│       └── vader.png
├── core
│   ├── collision.py
│   ├── phase_manager.py
│   ├── ranking.py
│   ├── score.py
│   └── spawner.py
├── entities
│   ├── enemy.py
│   ├── enemy_shot.py
│   ├── player.py
│   ├── powerup.py
│   └── spell.py
├── game.py
├── main.py
├── ranking.json
├── README.md
├── strategies
│   ├── boss_strategy.py
│   ├── movement_strategy.py
│   ├── stormtrooper_strategy.py
│   └── tie_strategy.py
├── ui
│   ├── hud.py
│   ├── menu_ship.py
│   ├── screens.py
│   └── starfield.py
└── utils
    └── assets.py
```

---

## 06 · Controles

| Tecla / Ação | Efeito |
|---|---|
| `← →` / `Mouse` | Move a nave |
| `Espaço` | Dispara |
| `P` | Pausa / continua |
| `ESC` | Pausa → Menu → Sair |
| `H` | Abre o Ranking (Top 10) |

---

## 07 · Instalação e Execução

**Requisitos:** Python 3.12 ou superior · Pygame

```bash
# Clonar o repositório
git clone https://github.com/Dudateic/galaxy_defense.git
cd galaxy_defense

# Instalar dependências
pip install pygame

# Executar
python main.py
```

---

<p align="center">Galaxy Defense · Classic Games · Projeto de Portfolio · 2026</p>