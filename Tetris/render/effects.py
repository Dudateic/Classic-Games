import random, math
import pygame
from config.settings import PIECE_COLORS, FLASH_DURATION, C_GOLD, C_ACCENT, C_DANGER

class Particle:
    def __init__(self, x, y, color, speed_scale=1.0, gravity=0.15, life_range=(20,45), size_range=(2.5,6.0)):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 5.0) * speed_scale
        self.x       = x
        self.y       = y
        self.vx      = math.cos(angle) * speed
        self.vy      = math.sin(angle) * speed
        self.gravity = gravity
        self.life    = random.randint(*life_range)
        self.max_life= self.life
        self.color   = color
        self.size    = random.uniform(*size_range)

    def update(self) -> bool:
        self.x  += self.vx
        self.y  += self.vy
        self.vy += self.gravity
        self.vx *= 0.98
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha  = int(255 * (self.life / self.max_life))
        radius = max(1, int(self.size * (self.life / self.max_life)))
        r, g, b = self.color
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (r, g, b, alpha), (radius, radius), radius)
        surface.blit(s, (int(self.x)-radius, int(self.y)-radius))



class StarParticle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(3, 10)
        self.x    = x
        self.y    = y
        self.vx   = math.cos(angle) * speed
        self.vy   = math.sin(angle) * speed
        self.life = random.randint(40, 90)
        self.max_life = self.life
        self.color = color
        self.size  = random.uniform(4, 12)
        self.rot   = random.uniform(0, 360)
        self.rot_v = random.uniform(-8, 8)

    def update(self) -> bool:
        self.x   += self.vx
        self.y   += self.vy
        self.vy  += 0.2
        self.vx  *= 0.97
        self.rot += self.rot_v
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha  = int(255 * (self.life / self.max_life))
        r, g, b = self.color
        s = pygame.Surface((int(self.size)*4, int(self.size)*4), pygame.SRCALPHA)
        cx = int(self.size)*2
        pts = []
        for i in range(10):
            a   = math.radians(self.rot + i * 36)
            rad = self.size if i % 2 == 0 else self.size * 0.4
            pts.append((cx + math.cos(a)*rad, cx + math.sin(a)*rad))
        if len(pts) >= 3:
            pygame.draw.polygon(s, (r, g, b, alpha), pts)
        surface.blit(s, (int(self.x)-cx, int(self.y)-cx))


class FloatingText:
    def __init__(self, x, y, text, color, size=22):
        self.x    = x
        self.y    = y
        self.vy   = -1.5
        self.text = text
        self.color= color
        self.size = size
        self.life = 70
        self.max_life = self.life
        self.font = pygame.font.SysFont('Consolas', size, bold=True)

    def update(self) -> bool:
        self.y   += self.vy
        self.vy  *= 0.97
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        r, g, b = self.color
        surf = self.font.render(self.text, True, (r, g, b))
        surf.set_alpha(alpha)
        surface.blit(surf, (int(self.x) - surf.get_width()//2, int(self.y)))


class EffectManager:
    def __init__(self):
        self.particles     = []
        self.texts         = []
        self.flashing_lines= {}
        self.screen_flash  = 0
        self.screen_flash_color = (255, 255, 255)
        self.shake_frames  = 0


    def spawn_line_clear(self, rows: list[int], board, cell_size: int,
                         offset_x: int, offset_y: int) -> None:
        for row in rows:
            self.flashing_lines[row] = FLASH_DURATION
            for col in range(len(board.grid[0])):
                cell  = board.grid[row][col]
                color = PIECE_COLORS.get(cell, (200, 200, 200))
                cx = offset_x + col * cell_size + cell_size // 2
                cy = offset_y + row * cell_size + cell_size // 2
                for _ in range(8):
                    self.particles.append(Particle(cx, cy, color, speed_scale=1.2))

    def spawn_tetris(self, board, cell_size, offset_x, offset_y, score_x, score_y):
        """ Efeito especial para 4 linhas (Tetris!). """
        self.screen_flash       = 10
        self.screen_flash_color = (0, 220, 140)
        self.texts.append(FloatingText(score_x, score_y - 60, 'TETRIS!!!',
                                       C_GOLD, size=32))
        for _ in range(80):
            x = random.randint(offset_x, offset_x + board.cols * cell_size)
            y = random.randint(offset_y, offset_y + board.rows * cell_size)
            c = random.choice(list(PIECE_COLORS.values()))
            self.particles.append(Particle(x, y, c, speed_scale=2.0,
                                           life_range=(30,70), size_range=(3,8)))

    def spawn_level_up(self, level: int, cx: int, cy: int):
        self.screen_flash       = 8
        self.screen_flash_color = C_ACCENT
        self.texts.append(FloatingText(cx, cy, f'NÍVEL {level}!', C_GOLD, size=28))
        for _ in range(40):
            self.particles.append(Particle(cx, cy, C_GOLD, speed_scale=1.8,
                                           life_range=(25,55), gravity=0.1))

    def spawn_piece_lock(self, cx: int, cy: int, color: tuple):
        for _ in range(6):
            self.particles.append(Particle(cx, cy, color, speed_scale=0.6,
                                           life_range=(10,25), gravity=0.2,
                                           size_range=(1.5, 3.5)))

    def spawn_bomb(self, cx: int, cy: int):
        self.screen_flash       = 15
        self.screen_flash_color = C_DANGER
        self.shake_frames = 20
        for _ in range(100):
            self.particles.append(Particle(cx, cy, C_DANGER, speed_scale=3.0,
                                           life_range=(20,60), size_range=(3,10)))
        for _ in range(40):
            self.particles.append(Particle(cx, cy, (255,200,0), speed_scale=2.0,
                                           life_range=(15,35), gravity=0.3))

    def spawn_celebration(self, w: int, h: int):
        colors = [C_GOLD, (255,80,80), (80,200,255), (80,255,120), (255,180,0)]
        for _ in range(120):
            x = random.randint(0, w)
            y = random.randint(-50, h//2)
            self.particles.append(StarParticle(x, y, random.choice(colors)))

    def spawn_combo(self, combo: int, cx: int, cy: int):
        if combo < 2:
            return
        self.texts.append(FloatingText(cx, cy - 30, f'COMBO x{combo}!',
                                       (255, 160, 0), size=24))

    def spawn_score_popup(self, pts: int, cx: int, cy: int):
        if pts <= 0:
            return
        self.texts.append(FloatingText(cx, cy, f'+{int(pts)}', C_ACCENT, size=20))


    def update(self) -> None:
        self.particles = [p for p in self.particles if p.update()]
        self.texts     = [t for t in self.texts     if t.update()]
        for row in list(self.flashing_lines):
            self.flashing_lines[row] -= 1
            if self.flashing_lines[row] <= 0:
                del self.flashing_lines[row]
        if self.screen_flash > 0:
            self.screen_flash -= 1
        if self.shake_frames > 0:
            self.shake_frames -= 1

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surface)
        for t in self.texts:
            t.draw(surface)
        if self.screen_flash > 0:
            alpha = int(120 * (self.screen_flash / 15))
            ov = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            r, g, b = self.screen_flash_color
            ov.fill((r, g, b, alpha))
            surface.blit(ov, (0, 0))

    @property
    def shake_offset(self) -> tuple[int,int]:
        if self.shake_frames <= 0:
            return (0, 0)
        mag = min(self.shake_frames, 8)
        return (random.randint(-mag, mag), random.randint(-mag, mag))
