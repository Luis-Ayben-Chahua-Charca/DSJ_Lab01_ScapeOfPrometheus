import math
import random

from bosses.boss import Boss, compute_fade_alpha
from bosses.projectile import BossProjectile
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import (
    BOSS_FADE_DURATION,
    BOSS_MAX_X,
    BOSS_MAX_Y,
    BOSS_MIN_X,
    BOSS_MIN_Y,
    BOSS_SIZE,
    LOKI_ATTACKS_PER_WALL,
    LOKI_BURST_COUNT,
    LOKI_BURST_INTERVAL,
    LOKI_FADE_DURATION,
    LOKI_FIRE_COOLDOWN,
    LOKI_GRACE_DURATION,
    LOKI_PARALLEL_GAP,
    LOKI_PARALLEL_SHOT_COUNT,
    LOKI_PROJECTILE_SPEED,
    LOKI_WALL_DRIFT_SPEED,
    LOKI_WALL_OFFSET,
    LOKI_WALLS,
)

_PATTERN_STRAIGHT = "straight"
_PATTERN_DIAGONAL = "diagonal"
_PATTERN_PARALLEL = "parallel"
_PATTERNS = [_PATTERN_STRAIGHT, _PATTERN_DIAGONAL, _PATTERN_PARALLEL]

# Dirección de disparo según la pared donde está apoyado: siempre hacia el
# lado contrario a esa pared, es decir, hacia adentro de la sala.
_WALL_FIRE_DIRECTION = {
    "top": (0, 1),
    "bottom": (0, -1),
    "left": (1, 0),
    "right": (-1, 0),
}

STATE_FADE_OUT = "fade_out"
STATE_FADE_IN = "fade_in"
STATE_GRACE = "grace"
STATE_WAITING = "waiting"
STATE_BURSTING = "bursting"

# Estados en los que el drift cosmético a lo largo de la pared está activo
# (se pausa durante el fade-out/fade-in, que es cuando "no está ahí").
_DRIFT_ACTIVE_STATES = {STATE_GRACE, STATE_WAITING, STATE_BURSTING}


class LokiBoss(Boss):
    """En cada parada: se desvanece, se teletransporta a una de las 4
    paredes al azar, reaparece, espera un momento de gracia sin atacar, y
    ejecuta LOKI_ATTACKS_PER_WALL ataques seguidos (patrón al azar entre los
    3 en cada uno) antes de volver a desvanecerse y cambiar de pared.
    Mientras está parado (gracia o entre ataques) tiene un leve vaivén
    cosmético a lo largo de la pared actual."""

    def __init__(self, screen, x, y):
        super().__init__(screen, "Loki", "Green_boss.png", x, y)

        self.wall = "top"
        self._reposition_on_wall(self.wall)
        self.fire_direction = _WALL_FIRE_DIRECTION[self.wall]
        self.drift_direction = 1

        self.state = STATE_GRACE
        self.state_timer = 0.0
        self.cooldown_remaining = LOKI_FIRE_COOLDOWN

        self.pending_pattern = None
        self.burst_shots_fired = 0
        self.attacks_done = 0

    def update(self, dt, player):
        self.tick_spawn_fade(dt)

        if self.state in _DRIFT_ACTIVE_STATES:
            self._tick_drift()

        if self.state == STATE_GRACE:
            self.state_timer += dt

            if self.state_timer >= LOKI_GRACE_DURATION:
                return self._begin_attack()

            return []

        if self.state == STATE_WAITING:
            self.cooldown_remaining -= dt

            if self.cooldown_remaining <= 0:
                return self._begin_attack()

            return []

        if self.state == STATE_BURSTING:
            self.state_timer += dt

            if self.burst_shots_fired >= LOKI_BURST_COUNT:
                self._finish_attack()
                return []

            if self.state_timer >= LOKI_BURST_INTERVAL:
                self.state_timer = 0.0
                return self._fire_straight_shot()

            return []

        if self.state == STATE_FADE_OUT:
            self.state_timer += dt

            if self.state_timer >= LOKI_FADE_DURATION:
                self._teleport_to_random_wall()
                self.attacks_done = 0
                self.state = STATE_FADE_IN
                self.state_timer = 0.0

            return []

        if self.state == STATE_FADE_IN:
            self.state_timer += dt

            if self.state_timer >= LOKI_FADE_DURATION:
                self.state = STATE_GRACE
                self.state_timer = 0.0

            return []

        return []

    def _begin_attack(self):
        self.pending_pattern = random.choice(_PATTERNS)

        if self.pending_pattern == _PATTERN_STRAIGHT:
            self.state = STATE_BURSTING
            self.state_timer = 0.0
            self.burst_shots_fired = 0
            return self._fire_straight_shot()

        projectiles = self._fire(self.pending_pattern)
        self._finish_attack()
        return projectiles

    def _finish_attack(self):
        self.attacks_done += 1
        self.pending_pattern = None

        if self.attacks_done >= LOKI_ATTACKS_PER_WALL:
            self.state = STATE_FADE_OUT
            self.state_timer = 0.0
        else:
            self.state = STATE_WAITING
            self.cooldown_remaining = LOKI_FIRE_COOLDOWN

    def _tick_drift(self):
        if self.wall in ("top", "bottom"):
            self.x += LOKI_WALL_DRIFT_SPEED * self.drift_direction
            if self.x <= BOSS_MIN_X:
                self.x = BOSS_MIN_X
                self.drift_direction = 1
            elif self.x >= BOSS_MAX_X:
                self.x = BOSS_MAX_X
                self.drift_direction = -1
        else:
            self.y += LOKI_WALL_DRIFT_SPEED * self.drift_direction
            if self.y <= BOSS_MIN_Y:
                self.y = BOSS_MIN_Y
                self.drift_direction = 1
            elif self.y >= BOSS_MAX_Y:
                self.y = BOSS_MAX_Y
                self.drift_direction = -1

    def _teleport_to_random_wall(self):
        self.wall = random.choice(LOKI_WALLS)
        self._reposition_on_wall(self.wall)
        self.fire_direction = _WALL_FIRE_DIRECTION[self.wall]

    def _reposition_on_wall(self, wall):
        if wall == "top":
            self.x = SCREEN_WIDTH / 2 - BOSS_SIZE / 2
            self.y = BOSS_MIN_Y + LOKI_WALL_OFFSET
        elif wall == "bottom":
            self.x = SCREEN_WIDTH / 2 - BOSS_SIZE / 2
            self.y = BOSS_MAX_Y - LOKI_WALL_OFFSET
        elif wall == "left":
            self.x = BOSS_MIN_X + LOKI_WALL_OFFSET
            self.y = SCREEN_HEIGHT / 2 - BOSS_SIZE / 2
        elif wall == "right":
            self.x = BOSS_MAX_X - LOKI_WALL_OFFSET
            self.y = SCREEN_HEIGHT / 2 - BOSS_SIZE / 2

    def _fire_origin(self):
        # Borde del sprite en la dirección de disparo, no el centro.
        center_x = self.x + BOSS_SIZE / 2
        center_y = self.y + BOSS_SIZE / 2
        dx, dy = self.fire_direction
        return center_x + dx * BOSS_SIZE / 2, center_y + dy * BOSS_SIZE / 2

    def _fire_straight_shot(self):
        self.burst_shots_fired += 1
        origin_x, origin_y = self._fire_origin()
        return [BossProjectile(self.screen, origin_x, origin_y, self.fire_direction, LOKI_PROJECTILE_SPEED)]

    def _fire(self, pattern):
        origin_x, origin_y = self._fire_origin()
        direction = self.fire_direction

        if pattern == _PATTERN_DIAGONAL:
            return [
                BossProjectile(self.screen, origin_x, origin_y, _rotate45(direction, -1), LOKI_PROJECTILE_SPEED),
                BossProjectile(self.screen, origin_x, origin_y, _rotate45(direction, 1), LOKI_PROJECTILE_SPEED),
            ]

        # Paralelo: el espaciado entre los 5 disparos va en el eje
        # perpendicular a la dirección de disparo (ya no asume "hacia abajo").
        perp_x, perp_y = -direction[1], direction[0]
        offset_start = -(LOKI_PARALLEL_SHOT_COUNT - 1) / 2 * LOKI_PARALLEL_GAP

        return [
            BossProjectile(
                self.screen,
                origin_x + perp_x * (offset_start + i * LOKI_PARALLEL_GAP),
                origin_y + perp_y * (offset_start + i * LOKI_PARALLEL_GAP),
                direction,
                LOKI_PROJECTILE_SPEED,
            )
            for i in range(LOKI_PARALLEL_SHOT_COUNT)
        ]

    def _current_alpha(self):
        # El fade-in de entrada (spawn) manda hasta que termina; después,
        # cada teletransporte se desvanece y reaparece con el mismo cálculo.
        if self.spawn_time < BOSS_FADE_DURATION:
            return self.fade_alpha

        if self.state == STATE_FADE_OUT:
            return compute_fade_alpha(self.state_timer, LOKI_FADE_DURATION, fading_in=False)
        if self.state == STATE_FADE_IN:
            return compute_fade_alpha(self.state_timer, LOKI_FADE_DURATION, fading_in=True)

        return 255

    def draw(self):
        self.image.set_alpha(self._current_alpha())
        self.screen.blit(self.image, (self.x, self.y))


def _rotate45(direction, sign):
    """Rota un vector unitario ±45°, usado para separar el patrón diagonal
    en dos proyectiles simétricos alrededor de la dirección principal."""
    dx, dy = direction
    angle = math.radians(45 * sign)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return (dx * cos_a - dy * sin_a, dx * sin_a + dy * cos_a)
