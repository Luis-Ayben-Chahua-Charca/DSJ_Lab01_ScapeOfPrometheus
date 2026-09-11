from data.config import ITEM_PICKUP_SIZE
from items.item import Item


class ProbePickup(Item):
    """Sonda: +50% de velocidad de movimiento, aditivo por copia (no compuesto)."""

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "sonda.png", ITEM_PICKUP_SIZE)

    def apply_to(self, player):
        player.speed_item_count += 1
        return True
