import random
import numpy as np
from config.settings import PIECE_COLORS

EMPTY = '⬛'

_RAW_PIECES = [

    [
        np.array([['⬜','⬜','⬜','⬜']]),
        np.array([['⬜'],['⬜'],['⬜'],['⬜']]),
    ],

    [
        np.array([['🟪','🟪'],
                  ['🟪','🟪']]),
    ],

    [
        np.array([[EMPTY,'🟧',EMPTY],
                  ['🟧', '🟧','🟧']]),
        np.array([['🟧',EMPTY],
                  ['🟧','🟧'],
                  ['🟧',EMPTY]]),
        np.array([['🟧','🟧','🟧'],
                  [EMPTY,'🟧',EMPTY]]),
        np.array([[EMPTY,'🟧'],
                  ['🟧', '🟧'],
                  [EMPTY,'🟧']]),
    ],

    [
        np.array([[EMPTY,EMPTY,'🟨'],
                  ['🟨', '🟨','🟨']]),
        np.array([['🟨',EMPTY],
                  ['🟨',EMPTY],
                  ['🟨','🟨']]),
        np.array([['🟨','🟨','🟨'],
                  ['🟨',EMPTY,EMPTY]]),
        np.array([['🟨','🟨'],
                  [EMPTY,'🟨'],
                  [EMPTY,'🟨']]),
    ],

    [
        np.array([['🟩',EMPTY,EMPTY],
                  ['🟩','🟩','🟩']]),
        np.array([['🟩','🟩'],
                  ['🟩',EMPTY],
                  ['🟩',EMPTY]]),
        np.array([['🟩','🟩','🟩'],
                  [EMPTY,EMPTY,'🟩']]),
        np.array([[EMPTY,'🟩'],
                  [EMPTY,'🟩'],
                  ['🟩','🟩']]),
    ],

    [
        np.array([[EMPTY,'🟦','🟦'],
                  ['🟦', '🟦',EMPTY]]),
        np.array([['🟦',EMPTY],
                  ['🟦','🟦'],
                  [EMPTY,'🟦']]),
    ],

    [
        np.array([['🟥','🟥',EMPTY],
                  [EMPTY,'🟥','🟥']]),
        np.array([[EMPTY,'🟥'],
                  ['🟥','🟥'],
                  ['🟥',EMPTY]]),
    ],

    [
        np.array([['💣']]),
    ],
]

_WEIGHTS = [14, 14, 14, 14, 14, 14, 14, 2]


class Piece:
    """ Entidade que representa um componente (ativo) no tabuleiro. """

    def __init__(self, templates: list[np.ndarray]):
        self._templates = templates
        self._rot_idx   = random.randint(0, len(templates) - 1)
        self.matrix     = templates[self._rot_idx].copy()

    @property
    def is_bomb(self) -> bool:
        return '💣' in self.matrix

    @property
    def rows(self) -> int:
        return len(self.matrix)

    @property
    def cols(self) -> int:
        return len(self.matrix[0])

    def rotate_cw(self) -> None:
        self._rot_idx = (self._rot_idx + 1) % len(self._templates)
        self.matrix   = self._templates[self._rot_idx].copy()

    def rotate_ccw(self) -> None:
        self._rot_idx = (self._rot_idx - 1) % len(self._templates)
        self.matrix   = self._templates[self._rot_idx].copy()

    def get_rotated_matrix(self) -> np.ndarray:
        next_idx = (self._rot_idx + 1) % len(self._templates)
        return self._templates[next_idx].copy()

    def get_color(self) -> tuple:
        from config.settings import PIECE_COLORS
        for row in self.matrix:
            for cell in row:
                if cell != EMPTY and cell in PIECE_COLORS:
                    return PIECE_COLORS[cell]
        return (200, 200, 200)


class PieceFactory:
    """ Classe estática focada na instanciação de novas peças. """

    @staticmethod
    def create_random() -> 'Piece':
        chosen = random.choices(_RAW_PIECES, weights=_WEIGHTS, k=1)[0]
        return Piece(chosen)

    @staticmethod
    def yield_cells(matrix: np.ndarray, row: int, col: int):
        for i, mrow in enumerate(matrix):
            for j, cell in enumerate(mrow):
                if cell != EMPTY:
                    yield row + i, col + j, cell
