from .movement_strategy import MovementStrategy


class StormtrooperMovement(MovementStrategy):

    SPEED = 2

    def move(self, enemy):
        enemy.y += self.SPEED
