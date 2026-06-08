"""
game.py — top-level game loop and state machine.

Responsibilities:
  - Own the Pygame window, clock and global state enum
  - Route input events to the correct handler
  - Call update / draw helpers from core/, ui/ and entities/

Everything else lives in its own module.
"""

import pygame

from core import (
    PhaseManager, Score, Ranking,
    check_spell_enemy, check_enemy_shot_player,
    check_enemy_player, check_powerup_player,
    spawn_enemy, maybe_spawn_shot, maybe_spawn_powerup,
    SPAWN_INTERVAL,
)
from entities.player import Player
from entities.spell import Spell
from entities.enemy_shot import EnemyShot

from ui import (
    HUD, MenuScreen,
    make_starfield, make_menu_ships,
    draw_name_input, draw_start_screen,
    draw_ranking_screen, draw_game_over,
)
from utils.assets import load_sprites, load_audio
from strategies.boss_strategy import BossMovement



class State:
    MENU         = "menu"
    NAME_INPUT   = "name_input"
    START_SCREEN = "start_screen"
    GAME         = "game"
    GAME_OVER    = "game_over"
    RANKING      = "ranking"



class Game:

    FPS        = 60
    BOSS_HP    = 500

    def __init__(self, screen):
        self.screen = screen
        self.clock  = pygame.time.Clock()
        sw, sh = screen.get_width(), screen.get_height()

        self.sprites = load_sprites(sw, sh)
        self.audio   = load_audio()

        font = pygame.font.SysFont("Arial", 24)
        self.menu        = MenuScreen()
        self.hud         = HUD(font)
        self.menu_stars  = make_starfield(sw, sh)
        self.game_stars  = make_starfield(sw, sh)
        self.menu_ships  = make_menu_ships(sw, sh, self.sprites["menu_ship"])

        self.phase_manager = PhaseManager()
        self.ranking       = Ranking()

        self.state       = State.MENU
        self.player_name = ""
        self.score       = Score()

        self._init_game_objects()


    def _init_game_objects(self):
        self.player      = Player(self.sprites["player"])
        self.enemies     = []
        self.spells      = []
        self.enemy_shots = []
        self.powerups    = []
        self.score.reset()
        self.phase_manager.phase = 1
        self._spawn_timer = 0
        self._powerups_state = {"double_shot": False, "shield": False, "laser": False}


    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                running = self._handle_event(event, running)

            self._update()
            self._draw()
            pygame.display.flip()


    def _handle_event(self, event, running):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state not in (State.MENU,):
                self.state = State.MENU
            return running

        handlers = {
            State.MENU:         self._event_menu,
            State.NAME_INPUT:   self._event_name_input,
            State.START_SCREEN: self._event_start_screen,
            State.GAME:         self._event_game,
            State.GAME_OVER:    self._event_game_over,
            State.RANKING:      lambda e: None,
        }
        handler = handlers.get(self.state)
        if handler:
            result = handler(event)
            if result is False:
                return False
        return running

    def _event_menu(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.menu.move_up()
        elif event.key == pygame.K_DOWN:
            self.menu.move_down()
        elif event.key == pygame.K_RETURN:
            choice = self.menu.get_selected()
            if choice == "START":
                self.player_name = ""
                self.state = State.NAME_INPUT
            elif choice == "RANKING":
                self.state = State.RANKING
            elif choice == "SAIR":
                return False

    def _event_name_input(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_RETURN and self.player_name:
            self.state = State.START_SCREEN
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif event.unicode.isprintable():
            self.player_name += event.unicode

    def _event_start_screen(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._init_game_objects()
            self.state = State.GAME

    def _event_game(self, event):
        if event.type != pygame.KEYDOWN or event.key != pygame.K_SPACE:
            return
        px = self.player.x + self.player.sprite.get_width() // 2
        if self._powerups_state["double_shot"]:
            self.spells += [Spell(self.player.x + 10, self.player.y),
                            Spell(self.player.x + 40, self.player.y)]
        else:
            self.spells.append(Spell(px, self.player.y))
        if self.audio["shoot"]:
            self.audio["shoot"].play()

    def _event_game_over(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_RETURN:
            self._init_game_objects()
            self.state = State.GAME
        elif event.key == pygame.K_ESCAPE:
            self.state = State.MENU


    def _update(self):
        if self.state != State.GAME:
            return

        sw, sh = self.screen.get_width(), self.screen.get_height()

        # player
        keys = pygame.key.get_pressed()
        self.player.move(keys, sw, sh)

        # spawn enemies
        self._spawn_timer += 1
        if self._spawn_timer >= SPAWN_INTERVAL:
            self._spawn_timer = 0
            enemy = spawn_enemy(
                self.phase_manager.phase, sw,
                self.enemies, self.sprites, 
                self.BOSS_HP,
            )
            if enemy:
                self.enemies.append(enemy)

        # spells
        for spell in self.spells[:]:
            spell.move()
            if spell.off_screen():
                self.spells.remove(spell)

        # enemies
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.y > sh:
                self.enemies.remove(enemy)
                self.score.subtract(10)
                self.hud.trigger_hit()
                self._check_game_over()
                continue
            maybe_spawn_shot(enemy, self.player, self.enemy_shots, EnemyShot)
            maybe_spawn_powerup(enemy, self.powerups)

        for shot in self.enemy_shots[:]:
            shot.move()
            if shot.off_screen(sh):
                self.enemy_shots.remove(shot)

        for pu in self.powerups[:]:
            pu.move()
            if pu.off_screen(sh):
                self.powerups.remove(pu)

        explosions = check_spell_enemy(self.spells, self.enemies, self.score)
        for (x, y) in explosions:
            self.hud.add_explosion(x, y)
            if self.audio["explosion"]:
                self.audio["explosion"].play()

        hit_by_shot = check_enemy_shot_player(self.enemy_shots, self.player, self.score, sh)
        if hit_by_shot:
            self.hud.trigger_hit()
            self._check_game_over()

        hit_by_enemy = check_enemy_player(self.enemies, self.player, self.score)
        if hit_by_enemy:
            self.hud.trigger_hit()
            self._check_game_over()

        collected = check_powerup_player(self.powerups, self.player)
        for kind in collected:
            self._powerups_state[{
                "shield": "shield",
                "double": "double_shot",
                "laser":  "laser",
            }.get(kind, kind)] = True

        self.phase_manager.update(int(self.score))

    def _check_game_over(self):
        if self.score.is_zero():
            self.ranking.add_score(self.player_name, self.score)
            self.state = State.GAME_OVER


    def _draw(self):
        self.screen.fill((0, 0, 20))

        draw = {
            State.MENU:         self._draw_menu,
            State.NAME_INPUT:   self._draw_name_input,
            State.START_SCREEN: self._draw_start_screen,
            State.RANKING:      self._draw_ranking,
            State.GAME:         self._draw_game,
            State.GAME_OVER:    self._draw_game_over,
        }
        draw.get(self.state, lambda: None)()

    def _draw_menu(self):
        self.menu.draw(self.screen, self.menu_stars)


    def _draw_name_input(self):
        draw_name_input(self.screen, self.menu_stars, self.player_name)

    def _draw_start_screen(self):
        draw_start_screen(self.screen, self.menu_stars, self.player_name)

    def _draw_ranking(self):
        draw_ranking_screen(self.screen, self.menu_stars, self.ranking.get_top())

    def _draw_game(self):
        self.screen.blit(self.sprites["background"], (0, 0))
        from ui.starfield import draw_starfield
        draw_starfield(self.screen, self.game_stars)

        self.player.draw(self.screen)
        for spell in self.spells:
            spell.draw(self.screen)
        for shot in self.enemy_shots:
            shot.draw(self.screen)
        for pu in self.powerups:
            pu.draw(self.screen)

        boss = next((e for e in self.enemies if isinstance(e.strategy, BossMovement)), None)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.hud.draw(self.screen, self.score, boss_enemy=boss)

    def _draw_game_over(self):
        self._draw_game()           # keep the game visible behind overlay
        draw_game_over(self.screen, self.score)
