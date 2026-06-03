"""Sistema de partículas para efeitos visuais ao destruir tijolos."""
import math
import random
import pygame
from typing import List


class Particle:
    def __init__(self, x: float, y: float, color: tuple) -> None:
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 5.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.4, 0.9)
        self.max_life = self.life
        self.radius = random.randint(2, 5)
        self.color = color
        self.gravity = 0.12

    def update(self, dt: float) -> bool:
        self.x  += self.vx
        self.y  += self.vy
        self.vy += self.gravity
        self.life -= dt
        return self.life > 0

    def draw(self, surface: pygame.Surface) -> None:
        alpha_ratio = max(0.0, self.life / self.max_life)
        r = max(1, int(self.radius * alpha_ratio))

        c = tuple(int(ch * alpha_ratio) for ch in self.color)
        pygame.draw.circle(surface, c, (int(self.x), int(self.y)), r)


class ParticleSystem:
    def __init__(self) -> None:
        self._particles: List[Particle] = []

    def emit(self, x: float, y: float, color: tuple, count: int = 12) -> None:
        for _ in range(count):
            self._particles.append(Particle(x, y, color))

    def update(self, dt: float) -> None:
        self._particles = [p for p in self._particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        for p in self._particles:
            p.draw(surface)

    def clear(self) -> None:
        self._particles.clear()
