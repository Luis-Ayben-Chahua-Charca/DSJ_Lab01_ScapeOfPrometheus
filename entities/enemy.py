import math

from core.asset_loader import load_image
from data.config import ENEMY_CHASE_SPEED, ENEMY_MAX_X, ENEMY_MAX_Y, ENEMY_MIN_X, ENEMY_MIN_Y
from entities.entity import Entity


class Enemy(Entity):
    # Multiplicador global sobre ENEMY_CHASE_SPEED (ítem Satélite). Es de
    # clase, no de instancia, para afectar a todos los enemigos existentes
    # y a los que se spawneen después en cualquier sala.
    chase_speed_multiplier = 1.0

    def __init__(self, screen, x, y):
        # La posición ya no se elige acá: systems.spawn decide dónde,
        # evitando puertas y al jugador.
        super().__init__(screen, load_image("enemy.png"), x, y)

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        speed = ENEMY_CHASE_SPEED * Enemy.chase_speed_multiplier

        if distance > 0:
            self.x += speed * dx / distance
            self.y += speed * dy / distance

        if self.x <= ENEMY_MIN_X:
            self.x = ENEMY_MIN_X
        elif self.x >= ENEMY_MAX_X:
            self.x = ENEMY_MAX_X

        if self.y <= ENEMY_MIN_Y:
            self.y = ENEMY_MIN_Y
        elif self.y >= ENEMY_MAX_Y:
            self.y = ENEMY_MAX_Y

    @classmethod
    def reset_chase_speed_multiplier(cls):
        cls.chase_speed_multiplier = 1.0
