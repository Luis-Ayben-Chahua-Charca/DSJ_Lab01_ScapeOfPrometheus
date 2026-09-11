from data.config import ITEM_PICKUP_SIZE
from items.item import Item


class AsteroidPickup(Item):
    """Asteroide: las balas del jugador atraviesan enemigos (piercing) en vez de destruirse al impactar."""

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "asteroide.png", ITEM_PICKUP_SIZE)

    def apply_to(self, player):
        player.pierces = True
        return True
