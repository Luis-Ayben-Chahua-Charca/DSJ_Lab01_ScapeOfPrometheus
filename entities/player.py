import math

import pygame

from core.asset_loader import load_image
from data.config import (
    FIRE_COOLDOWN_BASE,
    PLAYER_INVULNERABILITY_DURATION,
    PLAYER_MAX_HP,
    PLAYER_SIZE,
    PLAYER_SPEED,
    PLAYER_START_X,
    PLAYER_START_Y,
    ROTATION_LERP_FACTOR,
    SPEED_ITEM_BONUS,
)
from entities.entity import Entity

# Ángulo de pygame.transform.rotate (sentido antihorario) para cada dirección
# de disparo, asumiendo que el sprite de la nave apunta "arriba" en su
# orientación original (0°) — verificado visualmente sobre assets/images/nave.png.
_DIRECTION_ANGLES = {
    (0, -1): 0,  # arriba
    (-1, 0): 90,  # izquierda
    (0, 1): 180,  # abajo
    (1, 0): 270,  # derecha
}
DEFAULT_FACING_ANGLE = _DIRECTION_ANGLES[(0, -1)]


class Player(Entity):
    def __init__(self, screen):
        image = pygame.transform.smoothscale(load_image("nave.png"), (PLAYER_SIZE, PLAYER_SIZE))
        super().__init__(screen, image, PLAYER_START_X, PLAYER_START_Y)
        self.reset()

    def reset(self):
        """Vuelve al estado de una run nueva: posición, HP, techo de HP y todos los buffs de ítems."""
        self.x, self.y = PLAYER_START_X, PLAYER_START_Y
        self.x_change = 0
        self.y_change = 0
        self.max_hp = PLAYER_MAX_HP
        self.hp = PLAYER_MAX_HP
        self.invulnerable_time = 0.0
        self._flicker_counter = 0

        # Buffs de ítems (permanentes durante la run, se limpian solo al reiniciar).
        # Los "_count" existen incluso donde ya hay una señal derivada (ej.
        # fire_cooldown_multiplier) porque el HUD de ítems (ui/item_hud.py)
        # necesita saber CUÁNTAS copias se recogieron, no solo el efecto.
        self.speed_item_count = 0  # Sonda
        self.fire_cooldown_multiplier = 1.0  # Telescopio (efecto)
        self.telescope_count = 0  # Telescopio (para el HUD)
        self.pierces = False  # Asteroide
        self.satellite_count = 0  # Satélite (el efecto en sí es global, ver Enemy)
        self.astronaut_count = 0  # Astronauta

        # Disparo / orientación
        self.fire_cooldown_remaining = 0.0
        self.facing_angle = DEFAULT_FACING_ANGLE
        self.target_angle = DEFAULT_FACING_ANGLE

    @property
    def speed(self):
        return PLAYER_SPEED * (1 + SPEED_ITEM_BONUS * self.speed_item_count)

    def move(self):
        # Normaliza el vector de movimiento para que la diagonal no sea
        # más rápida (√2x) que moverse en línea recta.
        length = math.hypot(self.x_change, self.y_change)

        if length > 0:
            self.x += self.speed * self.x_change / length
            self.y += self.speed * self.y_change / length

    def effective_fire_cooldown(self):
        return FIRE_COOLDOWN_BASE * self.fire_cooldown_multiplier

    def can_fire(self):
        return self.fire_cooldown_remaining <= 0

    def register_shot(self, direction):
        self.fire_cooldown_remaining = self.effective_fire_cooldown()
        self.target_angle = _DIRECTION_ANGLES.get(direction, self.target_angle)

    def tick_cooldown(self, dt):
        if self.fire_cooldown_remaining > 0:
            self.fire_cooldown_remaining -= dt

    def tick_rotation(self):
        # Lerp angular simple: se acerca un % fijo por frame, tomando el
        # camino corto (evita que gire "la vuelta larga" al cruzar 0°/360°).
        diff = (self.target_angle - self.facing_angle + 180) % 360 - 180
        self.facing_angle = (self.facing_angle + diff * ROTATION_LERP_FACTOR) % 360

    def take_damage(self, amount=1):
        """Fuente de daño genérica: contacto con enemigo/jefe, proyectil de
        jefe, rayo de Anubis. Toda fuente de daño debe pasar por acá — es lo
        único que respeta la ventana de invulnerabilidad."""
        if self.invulnerable_time > 0:
            return

        self.hp -= amount
        self.invulnerable_time = PLAYER_INVULNERABILITY_DURATION

    def tick_invulnerability(self, dt):
        if self.invulnerable_time > 0:
            self.invulnerable_time = max(0.0, self.invulnerable_time - dt)
            # Contador aparte, solo para el parpadeo visual (cosmético) —
            # la duración real de la invulnerabilidad ya no depende de esto.
            self._flicker_counter += 1
        else:
            self._flicker_counter = 0

    @property
    def is_invulnerable(self):
        return self.invulnerable_time > 0

    @property
    def is_alive(self):
        return self.hp > 0

    def draw(self):
        # Parpadeo: mientras es invulnerable, solo se dibuja en frames pares.
        if self.is_invulnerable and self._flicker_counter % 2 != 0:
            return

        # Rota alrededor del centro de la nave (no del top-left) para que no
        # "salte" de posición al girar.
        rotated = pygame.transform.rotate(self.image, self.facing_angle)
        rect = rotated.get_rect(center=(self.x + PLAYER_SIZE / 2, self.y + PLAYER_SIZE / 2))
        self.screen.blit(rotated, rect)
