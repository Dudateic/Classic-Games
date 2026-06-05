import pygame

_XP_BG      = (50, 50, 50)
_XP_FG      = (0, 255, 0)
_XP_BORDER  = (255, 255, 255)

_BOSS_BG    = (100, 100, 100)
_BOSS_FG    = (255, 0, 0)
_BOSS_BORD  = (255, 255, 255)

_HIT_COLOR  = (255, 0, 0)
_EXP_COLOR  = (255, 150, 0)

HIT_FLASH_FRAMES = 15
HIT_FLASH_ALPHA  = 100

EXPLOSION_GROW  = 2
EXPLOSION_MAX_R = 40



class HUD:
    """Draws all in-game overlays: score, XP bar, boss bar, flash, explosions."""

    def __init__(self, font):
        self.font = font
        self.flash_frames = 0
        self.explosions: list[list] = []   # each entry: [x, y, radius]


    def trigger_hit(self):
        self.flash_frames = HIT_FLASH_FRAMES

    def add_explosion(self, x, y):
        self.explosions.append([x, y, 20])

    def draw(self, screen, score, boss_enemy=None):
        self._draw_score(screen, score)
        self._draw_xp_bar(screen, score)
        if boss_enemy:
            self._draw_boss_bar(screen, boss_enemy)
        self._draw_explosions(screen)
        self._draw_flash(screen)


    def _draw_score(self, screen, score):
        text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def _draw_xp_bar(self, screen, score):
        bar_w, bar_h = 200, 15
        x, y = 10, 40
        ratio = min(int(score) / 100, 1.0)

        pygame.draw.rect(screen, _XP_BG,    (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, _XP_FG,    (x, y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(screen, _XP_BORDER, (x, y, bar_w, bar_h), 2)

    def _draw_boss_bar(self, screen, enemy):
        if enemy.hp <= 0:
            return
        bar_w, bar_h = 300, 20
        x = screen.get_width() // 2 - bar_w // 2
        y = 50
        ratio = enemy.hp / enemy.max_hp

        pygame.draw.rect(screen, _BOSS_BG,   (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, _BOSS_FG,   (x, y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(screen, _BOSS_BORD, (x, y, bar_w, bar_h), 2)

        label = self.font.render("BOSS", True, (255, 255, 255))
        screen.blit(label, (x + bar_w // 2 - label.get_width() // 2, y + 1))

    def _draw_explosions(self, screen):
        for exp in self.explosions[:]:
            pygame.draw.circle(screen, _EXP_COLOR, (exp[0], exp[1]), exp[2])
            exp[2] += EXPLOSION_GROW
            if exp[2] > EXPLOSION_MAX_R:
                self.explosions.remove(exp)

    def _draw_flash(self, screen):
        if self.flash_frames > 0:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((*_HIT_COLOR, HIT_FLASH_ALPHA))
            screen.blit(overlay, (0, 0))
            self.flash_frames -= 1
