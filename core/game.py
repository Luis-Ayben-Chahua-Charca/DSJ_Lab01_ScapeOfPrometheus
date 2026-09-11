import random

import pygame

from bosses.boss_factory import BOSS_THEME_FILES, create_boss
from bosses.boss_pool import draw_next_boss
from core.asset_loader import load_image, load_sound
from core.constants import BLACK, CAPTION, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from core.music import MusicManager
from data.config import BOSS_MIN_Y, BOSS_SIZE, ITEM_DROP_CHANCE, PICKUP_SIZE, PLAYER_SIZE, SHIELD_DROP_CHANCE
from entities.enemy import Enemy
from entities.player import Player
from items.registry import ITEM_CLASSES
from items.shield_pickup import ShieldPickup
from rooms.room_manager import RoomManager
from systems.collision import is_collision, rects_collide
from systems.navigation import update_room_transitions
from systems.score import Score
from ui.boss_hud import BossHUD
from ui.game_over import GameOverScreen
from ui.hud import HUD
from ui.item_hud import ItemHUD
from ui.minimap import Minimap
from ui.room_renderer import draw_room
from ui.victory import VictoryScreen
from weapons.bullet import Bullet

# Soundtrack de exploración (assets/music/): suena en loop en todas las salas
# salvo boss_room, que tiene su propio tema por jefe (ver BOSS_THEME_FILES).
EXPLORATION_MUSIC = "soundtrack.mp3"

STATE_PLAYING = "playing"
STATE_VICTORY = "victory"
STATE_GAME_OVER = "game_over"

# Las flechas disparan en su dirección (auto-fire mientras se mantienen
# presionadas); WASD mueve al jugador. Si hay varias flechas sostenidas a la
# vez, se dispara en una sola dirección con esta prioridad fija (determinística,
# no aleatoria): arriba > abajo > izquierda > derecha.
FIRE_KEY_PRIORITY = [
    (pygame.K_UP, (0, -1)),
    (pygame.K_DOWN, (0, 1)),
    (pygame.K_LEFT, (-1, 0)),
    (pygame.K_RIGHT, (1, 0)),
]


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.transform.smoothscale(
            load_image("backround2.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.music = MusicManager()
        self.music.play_immediately(EXPLORATION_MUSIC)

        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(load_image("ufo.png"))

        self.player = Player(self.screen)
        self.bullets = []
        self.score = Score()

        self.room_manager = RoomManager(self.screen, self.player)

        self.boss = None
        self.boss_projectiles = []
        self.current_boss_id = draw_next_boss()

        self.hud = HUD()
        self.minimap = Minimap()
        self.item_hud = ItemHUD()
        self.boss_hud = BossHUD()
        self.game_over_screen = GameOverScreen()
        self.victory_screen = VictoryScreen()

        self.state = STATE_PLAYING
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.music.tick(dt)

            self.screen.fill(BLACK)
            self.screen.blit(self.background, (0, 0))

            self._handle_events()

            if self.state == STATE_PLAYING:
                self._update_playing(dt)
            elif self.state == STATE_VICTORY:
                self.victory_screen.draw(self.screen)
            elif self.state == STATE_GAME_OVER:
                self.game_over_screen.draw(self.screen)

            self.hud.show_hp(self.screen, self.player)
            self.hud.show_score(self.screen, self.score.value)
            self.item_hud.draw(self.screen, self.player)
            self.minimap.draw(self.screen, self.room_manager)

            pygame.display.update()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.x_change = -1
                if event.key == pygame.K_d:
                    self.player.x_change = 1
                if event.key == pygame.K_w:
                    self.player.y_change = -1
                if event.key == pygame.K_s:
                    self.player.y_change = 1

                # Atajos de desarrollador (sin pista visible al jugador,
                # solo para pruebas/demo).
                if self.state == STATE_PLAYING:
                    if event.key == pygame.K_g:
                        self._dev_skip_to_corridor()
                    if event.key == pygame.K_h:
                        self._dev_kill_current_boss()

                if self.state in (STATE_GAME_OVER, STATE_VICTORY):
                    if event.key == pygame.K_r:
                        self._reset_run()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    self.player.x_change = 0
                if event.key in (pygame.K_w, pygame.K_s):
                    self.player.y_change = 0

    def _update_playing(self, dt):
        self.player.tick_invulnerability(dt)
        self.player.tick_cooldown(dt)
        self.player.tick_rotation()
        self.player.move()
        update_room_transitions(self.player, self.room_manager)

        self._handle_shooting()

        draw_room(self.screen, self.room_manager.current_room)

        self._update_pickups()
        self._update_enemies()
        self._update_bullets()

        if self.room_manager.current_room_id == "boss_room":
            self._update_boss(dt)

        self.player.draw()

        if not self.player.is_alive:
            self.music.stop()
            load_sound("defeat.mp3").play()
            self.state = STATE_GAME_OVER

    def _handle_shooting(self):
        keys = pygame.key.get_pressed()

        direction = None
        for key, key_direction in FIRE_KEY_PRIORITY:
            if keys[key]:
                direction = key_direction
                break

        if direction is not None and self.player.can_fire():
            self.player.register_shot(direction)
            self.bullets.append(Bullet(self.screen, self.player, direction, self.player.pierces))

    def _update_bullets(self):
        for bullet in list(self.bullets):
            bullet.update()

            if bullet.is_off_screen():
                self.bullets.remove(bullet)
            else:
                bullet.draw()

    def _update_boss(self, dt):
        if self.boss is None:
            x = SCREEN_WIDTH / 2 - BOSS_SIZE / 2
            self.boss = create_boss(self.current_boss_id, self.screen, x, BOSS_MIN_Y)

            # Primera vez que se entra a boss_room en esta run: mismo punto
            # donde arranca el fade-in del sprite del jefe.
            load_sound("boss_appear.mp3").play()
            self.music.switch_to(BOSS_THEME_FILES[self.current_boss_id])

        boss = self.boss
        new_projectiles = boss.update(dt, self.player)
        self.boss_projectiles.extend(new_projectiles)

        # Bala del jugador (rect-based, no la distancia fija de enemigos
        # comunes) contra el jefe. Cada bala solo puede pegarle una vez en
        # toda su vida, incluso si perfora (Asteroide) y queda varios
        # frames superpuesta con un sprite grande.
        for bullet in list(self.bullets):
            if getattr(bullet, "hit_boss", False):
                continue

            if rects_collide(bullet, boss):
                boss.take_bullet_hit()
                bullet.hit_boss = True

                if not bullet.pierces:
                    self.bullets.remove(bullet)

        # Contacto directo jugador-jefe, igual que con enemigos comunes.
        if rects_collide(self.player, boss):
            self.player.take_damage()

        # Rayo de Anubis (u otro mecanismo de daño por superposición futuro).
        beam_rect = boss.get_beam_rect()
        if beam_rect is not None:
            player_rect = pygame.Rect(self.player.x, self.player.y, PLAYER_SIZE, PLAYER_SIZE)
            if beam_rect.colliderect(player_rect):
                self.player.take_damage()

        self._update_boss_projectiles()

        boss.draw()
        self.boss_hud.draw(self.screen, boss)

        if not boss.is_alive:
            # Reusa el mismo sonido de muerte de enemigo común (no hay un
            # asset dedicado para la derrota del jefe) — ver Agents.md.
            load_sound("explosion.wav").play()
            self.music.stop()
            load_sound("victory.mp3").play()
            self.state = STATE_VICTORY

    def _update_boss_projectiles(self):
        for projectile in list(self.boss_projectiles):
            projectile.update()

            if rects_collide(self.player, projectile):
                self.player.take_damage()
                self.boss_projectiles.remove(projectile)
                continue

            if projectile.is_off_screen():
                self.boss_projectiles.remove(projectile)
            else:
                projectile.draw()

    def _dev_skip_to_corridor(self):
        """Atajo de desarrollador (sin pista en pantalla): teletransporta al
        corredor contiguo al jefe y lo marca limpio para poder probar la
        sala del jefe rápido. Solo para pruebas/demo."""
        room = self.room_manager.rooms["corridor"]
        room.enemies = []
        room.spawned = True
        room.is_clear = True

        self.room_manager.visited.add("corridor")
        self.room_manager.current_room_id = "corridor"

        self.player.x = SCREEN_WIDTH / 2 - PLAYER_SIZE / 2
        self.player.y = SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2

    def _dev_kill_current_boss(self):
        """Atajo de desarrollador (sin pista en pantalla): mata al jefe
        actual al instante, mismo flujo que una derrota real. Solo para
        pruebas/demo."""
        if self.room_manager.current_room_id != "boss_room":
            return

        if self.boss is not None and self.boss.is_alive:
            self.boss.hp = 0

    def _update_enemies(self):
        room = self.room_manager.current_room

        for enemy in list(room.enemies):
            enemy.move(self.player.x, self.player.y)

            hit_bullet = self._find_colliding_bullet(enemy)
            if hit_bullet is not None:
                load_sound("explosion.wav").play()

                self.score.increment()
                death_x, death_y = enemy.x, enemy.y
                room.kill_enemy(enemy)

                if not hit_bullet.pierces and hit_bullet in self.bullets:
                    self.bullets.remove(hit_bullet)

                self._maybe_drop_loot(room, death_x, death_y)
                continue

            if rects_collide(self.player, enemy):
                self.player.take_damage()

            enemy.draw()

    def _find_colliding_bullet(self, enemy):
        for bullet in self.bullets:
            if is_collision(enemy.x, enemy.y, bullet.x, bullet.y):
                return bullet
        return None

    def _maybe_drop_loot(self, room, x, y):
        if random.random() < SHIELD_DROP_CHANCE:
            room.add_pickup(ShieldPickup(self.screen, x, y))

        if random.random() < ITEM_DROP_CHANCE:
            item_cls = random.choice(ITEM_CLASSES)
            # Pequeño offset para que no quede exactamente encimado con un escudo.
            room.add_pickup(item_cls(self.screen, x + PICKUP_SIZE, y))

    def _update_pickups(self):
        room = self.room_manager.current_room

        for pickup in list(room.pickups):
            if rects_collide(self.player, pickup) and pickup.apply_to(self.player):
                load_sound("grabbed_item.mp3").play()
                room.remove_pickup(pickup)
                continue

            pickup.draw()

    def _reset_run(self):
        self.player.reset()
        self.bullets = []
        self.score.reset()
        self.room_manager.reset()
        Enemy.reset_chase_speed_multiplier()
        self.music.play_immediately(EXPLORATION_MUSIC)

        self.boss = None
        self.boss_projectiles = []
        # La bolsa de jefes (bosses/boss_pool.py) es deliberadamente
        # independiente del ciclo de vida de la run: no se resetea acá.
        self.current_boss_id = draw_next_boss()

        self.state = STATE_PLAYING
