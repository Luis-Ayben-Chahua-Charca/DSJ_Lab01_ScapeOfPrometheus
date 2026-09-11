from data.config import ITEM_PICKUP_SIZE, SATELLITE_CHASE_MULTIPLIER_STEP, SATELLITE_MIN_CHASE_MULTIPLIER
from entities.enemy import Enemy
from items.item import Item


class SatellitePickup(Item):
    """Satélite: reduce la velocidad de persecución de TODOS los enemigos
    (actuales y futuros, en cualquier sala) multiplicando un valor global en Enemy."""

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "satelite.png", ITEM_PICKUP_SIZE)

    def apply_to(self, player):
        Enemy.chase_speed_multiplier = max(
            SATELLITE_MIN_CHASE_MULTIPLIER,
            Enemy.chase_speed_multiplier * SATELLITE_CHASE_MULTIPLIER_STEP,
        )
        player.satellite_count += 1
        return True
