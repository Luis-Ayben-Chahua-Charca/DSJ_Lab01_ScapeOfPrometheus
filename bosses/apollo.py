import math

import pygame

from bosses.boss import Boss
from bosses.projectile import BossProjectile
from data.config import (
    APOLLO_APPROACH_DURATION,
    APOLLO_APPROACH_SPEED,
    APOLLO_MIN_DISTANCE_TO_PLAYER,
    APOLLO_PROJECTILE_COUNT,
    APOLLO_PROJECTILE_SPEED,
    APOLLO_SPIN_DURATION,
    BOSS_MAX_X,
    BOSS_MAX_Y,
    BOSS_MIN_X,
    BOSS_MIN_Y,
    BOSS_SIZE,
)

STATE_APPROACH = "approach"
STATE_SPIN = "spin"

_DIAG = math.sqrt(2) / 2

# 8 direcciones a 45°: N, NE, E, SE, S, SO, O, NO.
_OCTAGONAL_DIRECTIONS = [
    (0, -1),
    (_DIAG, -_DIAG),
    (1, 0),
    (_DIAG, _DIAG),
    (0, 1),
    (-_DIAG, _DIAG),
    (-1, 0),
    (-_DIAG, -_DIAG),
]


class ApolloBoss(Boss):
    """Ciclo: se acerca brevemente -> gira sobre sí mismo (telegraph) ->
    dispara una ráfaga de 8 direcciones -> vuelve a acercarse."""

    def __init__(self, screen, x, y):
        super().__init__(screen, "Apolo", "Orange_boss.png", x, y)
        self.state = STATE_APPROACH
        self.state_timer = 0.0
        self.rotation = 0.0

    def update(self, dt, player):
        self.tick_spawn_fade(dt)
        self.state_timer += dt

        if self.state == STATE_APPROACH:
            self._approach(player)

            if self.state_timer >= APOLLO_APPROACH_DURATION:
                self.state = STATE_SPIN
                self.state_timer = 0.0

        elif self.state == STATE_SPIN:
            self.rotation = (self.rotation + (360 / APOLLO_SPIN_DURATION) * dt) % 360

            if self.state_timer >= APOLLO_SPIN_DURATION:
                projectiles = self._fire_burst()
                self.state = STATE_APPROACH
                self.state_timer = 0.0
                return projectiles

        return []

    def _approach(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance > APOLLO_MIN_DISTANCE_TO_PLAYER:
            self.x += APOLLO_APPROACH_SPEED * dx / distance
            self.y += APOLLO_APPROACH_SPEED * dy / distance

        if self.x < BOSS_MIN_X:
            self.x = BOSS_MIN_X
        elif self.x > BOSS_MAX_X:
            self.x = BOSS_MAX_X

        if self.y < BOSS_MIN_Y:
            self.y = BOSS_MIN_Y
        elif self.y > BOSS_MAX_Y:
            self.y = BOSS_MAX_Y

    def _fire_burst(self):
        center_x = self.x + BOSS_SIZE / 2
        center_y = self.y + BOSS_SIZE / 2

        return [
            BossProjectile(self.screen, center_x, center_y, direction, APOLLO_PROJECTILE_SPEED)
            for direction in _OCTAGONAL_DIRECTIONS
        ][:APOLLO_PROJECTILE_COUNT]

    def draw(self):
        rotated = pygame.transform.rotate(self.image, self.rotation)
        rotated.set_alpha(self.fade_alpha)
        rect = rotated.get_rect(center=(self.x + BOSS_SIZE / 2, self.y + BOSS_SIZE / 2))
        self.screen.blit(rotated, rect)
