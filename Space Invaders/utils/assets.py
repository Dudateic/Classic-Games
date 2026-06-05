"""
Asset loader — loads all sprites, sounds and music from disk.
Returns typed dicts so every module knows exactly what keys exist.
"""

import pygame

_SPRITE_DIR = "assets/sprites"
_SOUND_DIR  = "assets/sounds"


def _load_image(path, fallback_color=(200, 200, 255), fallback_size=(50, 50)):
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        surf = pygame.Surface(fallback_size)
        surf.fill(fallback_color)
        return surf


def _load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


def load_sprites(screen_width, screen_height):
    bg_raw = _load_image(f"{_SPRITE_DIR}/background.png", (0, 0, 20), (screen_width, screen_height))
    return {
        "player":    _load_image(f"{_SPRITE_DIR}/player.png",      (0, 200, 0)),
        "storm":     _load_image(f"{_SPRITE_DIR}/stormtrooper.png", (200, 200, 200)),
        "tie":       _load_image(f"{_SPRITE_DIR}/tie.png",          (150, 150, 255)),
        "vader":     _load_image(f"{_SPRITE_DIR}/vader.png",        (200, 0, 0)),
        "menu_ship": _load_image(f"{_SPRITE_DIR}/menu_ship.png",    (200, 200, 255)),
        "background": pygame.transform.scale(bg_raw, (screen_width, screen_height)),
    }


def load_audio():
    pygame.mixer.init()
    shoot     = _load_sound(f"{_SOUND_DIR}/shoot.wav")
    explosion = _load_sound(f"{_SOUND_DIR}/explosion.wav")
    try:
        pygame.mixer.music.load(f"{_SOUND_DIR}/music.mp3")
        pygame.mixer.music.play(-1)
    except Exception:
        pass
    return {"shoot": shoot, "explosion": explosion}
