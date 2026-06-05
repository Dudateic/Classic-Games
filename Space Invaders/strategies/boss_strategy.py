import math
from .movement_strategy import MovementStrategy


class BossMovement(MovementStrategy):

    def __init__(self, amplitude=2, speed=0.05):
        self.t = 0
        self.amplitude = amplitude
        self.speed = speed

    def move(self, enemy):
        enemy.x += math.sin(self.t) * self.amplitude
        self.t += self.speed
