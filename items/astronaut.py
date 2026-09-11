from data.config import ASTRONAUT_BONUS_HP, ITEM_PICKUP_SIZE
from items.item import Item


class AstronautPickup(Item):
    """Astronauta: otorga 2 contenedores de escudo vacíos (sube el techo, no cura)."""

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "astronauta.png", ITEM_PICKUP_SIZE)

    def apply_to(self, player):
        player.max_hp += ASTRONAUT_BONUS_HP
        player.astronaut_count += 1
        return True
