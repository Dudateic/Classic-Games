import pygame
from core.config import Color


class Brick:

    def __init__(self, rect: pygame.Rect, row: int, total_rows: int, hp: int = 1) -> None:
        self.rect       = rect
        self.alive      = True
        self.hp         = hp
        self.max_hp     = hp
        self._row       = row
        self.color      = Color.BRICK_ROWS[row % len(Color.BRICK_ROWS)]
        self.points     = (total_rows - row) * 10 * hp

    def hit(self) -> int:
        """Aplica um impacto. Retorna pontos se destruído, 0 caso contrário."""
        if not self.alive:
            return 0
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return self.points
        return 0

    def destroy(self) -> int:
        self.alive = False
        return self.points

    def draw(self, surface: pygame.Surface) -> None:
        if not self.alive:
            return
        if self.max_hp > 1:
            ratio = self.hp / self.max_hp
            c = tuple(int(ch * (0.4 + 0.6 * ratio)) for ch in self.color)
        else:
            c = self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=4)
        pygame.draw.rect(surface, Color.GRAY, self.rect, width=1, border_radius=4)
        if self.max_hp > 1 and self.alive:
            font = pygame.font.SysFont("monospace", 11, bold=True)
            surf = font.render(str(self.hp), True, Color.WHITE)
            surface.blit(surf, (self.rect.centerx - surf.get_width() // 2,
                                self.rect.centery - surf.get_height() // 2))
