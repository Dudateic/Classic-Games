import numpy as np

class Board:
    """ Representação dos objetos do tabuleiro. """

    def __init__(self, rows: int, cols: int, empty_char: str = '⬛'):
        self.rows  = rows
        self.cols  = cols
        self.empty = empty_char
        self.grid  = [[self.empty] * self.cols for _ in range(self.rows)]

    def has_collision(self, matrix: np.ndarray, row: int, col: int) -> bool:
        for r_idx, grid_row in enumerate(matrix):
            for c_idx, cell in enumerate(grid_row):
                if cell != self.empty:
                    br = row + r_idx
                    bc = col + c_idx
                    if br < 0 or br >= self.rows or bc < 0 or bc >= self.cols:
                        return True
                    if self.grid[br][bc] != self.empty:
                        return True
        return False

    def stamp_piece(self, matrix: np.ndarray, row: int, col: int) -> None:
        for r_idx, grid_row in enumerate(matrix):
            for c_idx, cell in enumerate(grid_row):
                if cell != self.empty:
                    br = row + r_idx
                    bc = col + c_idx
                    if 0 <= br < self.rows and 0 <= bc < self.cols:
                        self.grid[br][bc] = cell

    def clear_full_lines(self) -> tuple[int, list[int]]:
        lines_to_clear = [i for i, row in enumerate(self.grid) if self.empty not in row]
        if not lines_to_clear:
            return 0, []
        surviving = [row for i, row in enumerate(self.grid) if i not in lines_to_clear]
        new_rows   = [[self.empty] * self.cols for _ in range(len(lines_to_clear))]
        self.grid  = new_rows + surviving
        return len(lines_to_clear), lines_to_clear

    def explode(self, center_row: int, center_col: int, radius: int = 2) -> None:
        for r in range(center_row - radius, center_row + radius + 1):
            for c in range(center_col - radius, center_col + radius + 1):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.grid[r][c] = self.empty

    def reset(self) -> None:
        self.grid = [[self.empty] * self.cols for _ in range(self.rows)]
