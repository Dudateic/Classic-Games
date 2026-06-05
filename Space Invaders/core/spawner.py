import random

from entities.enemy import Enemy
from entities.powerup import PowerUp
from strategies.stormtrooper_strategy import StormtrooperMovement
from strategies.tie_strategy import TieMovement
from strategies.boss_strategy import BossMovement

SPAWN_INTERVAL = 80        # frames between enemy spawns
SHOT_CHANCE = 80          # 1-in-N chance per enemy per frame
POWERUP_CHANCE = 500       # 1-in-N chance per enemy per frame
MIN_ENEMY_GAP = 80         # minimum horizontal gap between enemies


def _pick_x(screen_width, enemies, sprite_width=64):
    """Try to find an x position that doesn't overlap existing enemies."""
    for _ in range(10):
        x = random.randint(0, screen_width - sprite_width)
        if all(abs(e.x - x) >= MIN_ENEMY_GAP for e in enemies):
            return x
    return random.randint(0, screen_width - sprite_width)


def spawn_enemy(phase, screen_width, enemies, sprites, boss_hp):
    """Create and return a new Enemy for the given phase."""
    x = _pick_x(screen_width, enemies)

    if phase == 1:
        return Enemy(x, 0, sprites["storm"], StormtrooperMovement(), hp=1, points=10)

    if phase == 2:
        return Enemy(x, 0, sprites["tie"], TieMovement(), hp=2, points=20)

    if phase >= 3:
        boss_exists = any(isinstance(e.strategy, BossMovement) for e in enemies)        
        if not boss_exists:
            return Enemy(screen_width // 2, 50, sprites["vader"], BossMovement(), hp=boss_hp, points=200) 

    return None

def maybe_spawn_shot(enemy, player, enemy_shots, EnemyShot):
    """Randomly fire a shot from enemy toward player."""
    if random.randint(0, SHOT_CHANCE) != 1:
        return
    sx = enemy.x + enemy.sprite.get_width() // 4
    sy = enemy.y + enemy.sprite.get_height() // 4
    tx = player.x + player.sprite.get_width() // 2
    ty = player.y + player.sprite.get_height() // 2
    enemy_shots.append(EnemyShot(sx, sy, tx, ty, speed=5))


def maybe_spawn_powerup(enemy, powerups):
    """Randomly drop a powerup from enemy."""
    if random.randint(0, POWERUP_CHANCE) == 1:
        powerups.append(PowerUp(enemy.x, enemy.y))
