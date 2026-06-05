import math
from .movement_strategy import MovementStrategy


class TieMovement(MovementStrategy):

    def __init__(self, speed=3, amplitude=60, frequency=0.05):
        self.speed = speed
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_x = None
        self.time = 0

    def move(self, enemy):
        if self.start_x is None:
            self.start_x = enemy.x

        self.time += 1
        enemy.y += self.speed
        enemy.x = self.start_x + self.amplitude * math.sin(self.time * self.frequency)
