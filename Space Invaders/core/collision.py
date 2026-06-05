"""Collision detection helpers.

Each function receives the relevant lists and mutates them in-place,
returning events (e.g. explosions to spawn) so callers stay decoupled.
"""


def check_spell_enemy(spells, enemies, score):
    """Returns list of (x, y) positions where enemies were destroyed."""
    explosions = []

    for spell in spells[:]:
        for enemy in enemies[:]:
            if not spell.get_rect().colliderect(enemy.get_rect()):
                continue

            enemy.hp -= 1
            if spell in spells:
                spells.remove(spell)

            if enemy.hp <= 0:
                enemies.remove(enemy)
                score.add(enemy.points)
                explosions.append((enemy.x, enemy.y))

            break  # spell already consumed

    return explosions


def check_enemy_shot_player(enemy_shots, player, score, screen_height):
    """Returns True if a shot hit the player."""
    hit = False
    for shot in enemy_shots[:]:
        if shot.off_screen(screen_height):
            enemy_shots.remove(shot)
            continue
        if shot.get_rect().colliderect(player.get_rect()):
            score.subtract(20)
            enemy_shots.remove(shot)
            hit = True
    return hit


def check_enemy_player(enemies, player, score):
    """Returns True if any enemy collided with the player."""
    hit = False
    for enemy in enemies[:]:
        if enemy.get_rect().colliderect(player.get_rect()):
            enemies.remove(enemy)
            score.subtract(10)
            hit = True
    return hit


def check_powerup_player(powerups, player):
    """Returns list of powerup types collected."""
    collected = []
    for powerup in powerups[:]:
        if powerup.get_rect().colliderect(player.get_rect()):
            collected.append(powerup.kind)
            powerups.remove(powerup)
    return collected
