import math
import random

from data.config import (
    DOOR_BAND_X,
    DOOR_BAND_Y,
    DOOR_SPAWN_EXCLUSION,
    ENEMY_MAX_X,
    ENEMY_MAX_Y,
    ENEMY_MIN_X,
    ENEMY_MIN_Y,
    ENEMY_SPAWN_MIN_DISTANCE_FROM_PLAYER,
)
from entities.enemy import Enemy

MAX_SPAWN_ATTEMPTS = 20


def spawn_enemies(screen, count, player=None):
    return [Enemy(screen, *_pick_spawn_position(player)) for _ in range(count)]


def _pick_spawn_position(player):
    """Rechazo por muestreo: evita las 4 zonas de puerta y un radio
    alrededor del jugador. Si se agotan los intentos, usa la última
    candidata igual (para no colgar el juego)."""
    x = y = None

    for _ in range(MAX_SPAWN_ATTEMPTS):
        x = random.randint(ENEMY_MIN_X, ENEMY_MAX_X)
        y = random.randint(ENEMY_MIN_Y, ENEMY_MAX_Y)

        if not _too_close_to_a_door(x, y) and not _too_close_to_player(x, y, player):
            break

    return x, y


def _too_close_to_a_door(x, y):
    band_x_min = DOOR_BAND_X[0] - DOOR_SPAWN_EXCLUSION
    band_x_max = DOOR_BAND_X[1] + DOOR_SPAWN_EXCLUSION
    band_y_min = DOOR_BAND_Y[0] - DOOR_SPAWN_EXCLUSION
    band_y_max = DOOR_BAND_Y[1] + DOOR_SPAWN_EXCLUSION

    near_top = y <= ENEMY_MIN_Y + DOOR_SPAWN_EXCLUSION and band_x_min <= x <= band_x_max
    near_bottom = y >= ENEMY_MAX_Y - DOOR_SPAWN_EXCLUSION and band_x_min <= x <= band_x_max
    near_left = x <= ENEMY_MIN_X + DOOR_SPAWN_EXCLUSION and band_y_min <= y <= band_y_max
    near_right = x >= ENEMY_MAX_X - DOOR_SPAWN_EXCLUSION and band_y_min <= y <= band_y_max

    return near_top or near_bottom or near_left or near_right


def _too_close_to_player(x, y, player):
    if player is None:
        return False

    return math.hypot(x - player.x, y - player.y) < ENEMY_SPAWN_MIN_DISTANCE_FROM_PLAYER
