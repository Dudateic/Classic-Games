# Tetris

> Sistema de organização espacial sob restrição, baseado em encaixe e otimização de espaço em tempo real

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-latest-013243?style=flat-square&logo=numpy)
![FPS](https://img.shields.io/badge/60_FPS-determinístico-00ffaa?style=flat-square)
![Status](https://img.shields.io/badge/status-completo-brightgreen?style=flat-square)

---

## Sumário

- [01 · Conceito Central](#01--conceito-central)
- [02 · Mecânicas Principais](#02--mecânicas-principais)
- [03 · Sistema de Peças](#03--sistema-de-peças)
- [04 · Sistema de Pontuação](#04--sistema-de-pontuação)
- [05 · Módulos do Sistema](#05--módulos-do-sistema)
- [06 · Efeitos Visuais](#06--efeitos-visuais)
- [07 · Máquina de Estados](#07--máquina-de-estados)
- [08 · Controles](#08--controles)
- [09 · Fluxo de Execução](#09--fluxo-de-execução)
- [10 · Instalação e Execução](#10--instalação-e-execução)

---

## 01 · Conceito Central

O Tetris Engine é projetado como um **sistema interativo baseado em simulação discreta**, no qual o estado do jogo evolui por meio de regras determinísticas e entradas do usuário interpretadas como intenções formais.

O sistema opera como uma **máquina de transformação de estado**: o jogador não manipula diretamente o mundo — ele emite intenções. O motor valida, simula e resolve essas intenções a cada tick de simulação. Essa separação estrita entre **ação humana** e **simulação computacional** garante determinismo completo e reprodutibilidade integral de qualquer sessão.

| Peças | Módulos | FPS | Níveis |
|:-----:|:-------:|:---:|:------:|
| 7 + 1 especial | 8 | 60 | ilimitado |

---

## 02 · Mecânicas Principais

| Mecânica | Descrição |
|----------|-----------|
| **Gravidade** | Queda progressiva baseada no nível atual. Velocidade calculada em ticks por frame. |
| **Lock Delay** | Janela de 20 ticks para ajustes finais antes da fixação da peça ao tabuleiro. |
| **Ghost Piece** | Projeção visual da posição de pouso da peça ativa, auxiliando o planejamento espacial. |
| **Hold System** | Armazenamento e troca estratégica de peças. Permitido uma vez por peça ativa. |
| **Hard Drop** | Fixação instantânea com bônus de pontuação proporcional à distância percorrida. |
| **Rotação CW/CCW** | Rotação horária e anti-horária com validação automática de colisão. |
| **Peca Especial** | Peça com probabilidade de 2% que destrói uma área de 5x5 células ao fixar. |
| **Next Queue** | Fila de visualização das três próximas peças para planejamento antecipado. |

---

## 03 · Sistema de Peças

O sistema contempla as sete peças canônicas do Tetris acrescidas de uma peça especial, todas representadas como arrays NumPy com rotações pré-computadas e geração ponderada.

| Peça | Nome | Rotações |
|:----:|------|:--------:|
| I | Barra | 2 |
| O | Quadrado | 1 |
| T | Te | 4 |
| L | Ele | 4 |
| J | Jota | 4 |
| S | Esse | 2 |
| Z | Ze | 2 |
| Especial | Bomba | — · 2% de probabilidade |

---

## 04 · Sistema de Pontuação

| Acao | Pontos Base | Multiplicador |
|------|-------------|---------------|
| 1 linha | 100 pts | x nivel |
| 2 linhas | 300 pts | x nivel |
| 3 linhas | 500 pts | x nivel |
| 4 linhas (Tetris) | 800 pts | x nivel |
| Hard Drop | +2 x distancia | — |
| Bonus de combo | 50 x combo x nivel | cumulativo |

**Progressão de nível:** a cada 10 linhas eliminadas, o nível avança e a velocidade de queda aumenta. A velocidade é calculada pela expressão `max(4, 48 − (nível − 1) × 4)` ticks por frame.

---

## 05 · Módulos do Sistema

| Módulo | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| **Board** | `core/board.py` | Grade 22x10, detecção de colisões, fixação de peças, eliminação de linhas e explosão de área. |
| **Pieces** | `core/pieces.py` | Definição das peças como arrays NumPy, rotação CW/CCW, factory ponderada e geração de ghost. |
| **Scoring** | `core/scoring.py` | Cálculo de pontuação com combos e multiplicadores de nível. Leaderboard persistido em JSON. |
| **GameEngine** | `engine/game_loop.py` | Orquestrador central: loop a 60 FPS, máquina de estados, física e controle de lock delay. |
| **InputManager** | `engine/input_handler.py` | Captura e normalização de eventos de teclado. Distingue eventos discretos (KEYDOWN) de estado contínuo (key held). |
| **RenderPipeline** | `render/renderer.py` | Projeção visual do estado interno: tabuleiro, ghost, hold, next queue, HUD e telas de transição. |
| **EffectManager** | `render/effects.py` | Sistema de partículas, textos flutuantes, flash de tela, tremor de câmera e animação de recorde. |
| **Settings** | `config/settings.py` | Constantes globais calculadas dinamicamente a partir da resolução do monitor em uso. |

---

## 06 · Efeitos Visuais

| Efeito | Ativador | Descrição |
|--------|----------|-----------|
| `spawn_line_clear` | Linha eliminada | Partículas coloridas emitidas de cada célula removida. |
| `spawn_tetris` | 4 linhas simultâneas | Flash de tela verde, exibição de texto e emissão de 80 partículas. |
| `spawn_level_up` | Novo nível | Flash dourado, exibição do novo nível e chuva de partículas douradas. |
| `spawn_bomb` | Fixação da peça especial | Flash vermelho, tremor de câmera e 140 partículas de alta velocidade. |
| `spawn_combo` | Combo igual ou superior a 2 | Texto flutuante indicando o multiplicador de combo ativo. |
| `spawn_celebration` | Novo recorde registrado | 120 partículas em queda cobrindo toda a área de jogo. |

---

## 07 · Máquina de Estados

```
name_entry --> game --> game_over --> leaderboard --> celebration
                  ^__________________________|
```

| Estado | Descrição |
|--------|-----------|
| `name_entry` | Entrada do nome do jogador antes do início da partida. |
| `game` | Sessão ativa de jogo em execução. |
| `game_over` | Exibição do resultado final da partida encerrada. |
| `leaderboard` | Visualização do ranking de pontuações armazenadas. |
| `celebration` | Animação de recorde ao superar a melhor pontuação registrada. |

---

## 08 · Controles

| Tecla | Ação |
|-------|------|
| `Seta Esquerda` / `Seta Direita` | Deslocar a peça lateralmente |
| `Seta Abaixo` (mantida) | Soft drop — queda acelerada |
| `Barra de Espaço` | Hard drop — fixação imediata |
| `Seta Acima` | Rotação horária (CW) |
| `Z` | Rotação anti-horária (CCW) |
| `C` / `Shift` | Hold — armazenar ou trocar a peça ativa |
| `P` | Pausar / retomar a partida |
| `Enter` | Confirmar entrada ou reiniciar partida |
| `Esc` | Encerrar o jogo |

---

## 09 · Fluxo de Execução

```
InputManager.poll()
  --> GameEngine._process_movement()
    --> _update_physics()
      --> Board.stamp() / Board.clear_full_lines()
        --> Scorer.add_lines()
          --> EffectManager.update()
            --> RenderPipeline.render()
```

<details>
<summary>Arvore de chamadas completa</summary>

```
main.py
  └── Application.run()
        └── GameEngine.start()
              ├── InputManager.poll_events()
              ├── _update_game()
              │     ├── _process_movement()
              │     │     ├── Board.has_collision()
              │     │     └── Piece.rotate_cw / rotate_ccw()
              │     └── _update_physics()
              │           ├── gravity + fall_counter
              │           └── _lock_piece()
              │                 ├── Board.stamp_piece()
              │                 ├── Board.clear_full_lines()
              │                 ├── Scorer.add_lines()
              │                 └── EffectManager.spawn_*()
              └── RenderPipeline.render_frame()
```

</details>

---

## 10 · Instalação e Execução

**Requisitos:** Python 3.10 ou superior · Pygame 2.x · NumPy · Monitor Full HD recomendado

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/games-classic.git
cd games-classic/Tetris

# 2. Instalar dependências
pip install pygame numpy

# 3. Executar
python main.py
```

---

<p align="center">Tetris · Classic Games · Projeto de Portfolio · 2026</p>