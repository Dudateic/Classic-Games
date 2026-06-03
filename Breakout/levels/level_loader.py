from typing import List, Optional
import random
from core.config import BRICK_COLS, BRICK_ROWS as BRICK_ROW_COUNT

"""Carregador de níveis – define layouts de tijolos diferentes por nível."""


_LAYOUTS = [
    None,

    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    ],

    [
        [1, 0, 2, 0, 3, 3, 0, 4, 0, 5],
        [1, 0, 2, 0, 3, 3, 0, 4, 0, 5],
        [1, 0, 2, 0, 3, 3, 0, 4, 0, 5],
        [1, 0, 2, 0, 3, 3, 0, 4, 0, 5],
        [6, 0, 6, 0, 6, 6, 0, 6, 0, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    ],

    [
        [1, 0, 0, 0, 2, 2, 0, 0, 0, 1],
        [0, 3, 0, 0, 4, 4, 0, 0, 3, 0],
        [0, 0, 5, 0, 5, 5, 0, 5, 0, 0],
        [0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
        [0, 0, 5, 0, 5, 5, 0, 5, 0, 0],
        [0, 3, 0, 0, 4, 4, 0, 0, 3, 0],
    ],

    [
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 4],
        [4, 3, 2, 1, 6, 5, 4, 3, 2, 1],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ],
]


def get_layout(level: int) -> Optional[List[List[int]]]:
    """Retorna o layout para o nível (1-indexado).
    Retorna None para grade clássica / aleatória."""
    idx = (level - 1) % len(_LAYOUTS)
    layout = _LAYOUTS[idx]
    if layout is None and level > len(_LAYOUTS):
        return _random_layout(level)
    return layout


def _random_layout(level: int) -> List[List[int]]:
    """Gera layout pseudo-aleatório baseado no nível."""
    rng = random.Random(level * 1337)
    patterns = [
        lambda r, c: rng.random() > 0.3,
        lambda r, c: (r + c) % 2 == 0,
        lambda r, c: c < BRICK_COLS // 2 or rng.random() > 0.5,
        lambda r, c: abs(c - BRICK_COLS // 2) < r + 1,
    ]
    pattern = patterns[level % len(patterns)]
    grid = []
    for r in range(BRICK_ROW_COUNT):
        row = []
        for c in range(BRICK_COLS):
            if pattern(r, c):
                hp = 1
                if level > 3 and rng.random() < 0.2:
                    hp = 2
                if level > 5 and rng.random() < 0.1:
                    hp = 3
                row.append(hp + 7 if hp > 1 else (r % 6 + 1))
            else:
                row.append(0)
        grid.append(row)
    return grid
