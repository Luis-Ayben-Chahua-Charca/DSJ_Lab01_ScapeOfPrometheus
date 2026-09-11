from data.config import PICKUP_SIZE
from items.item import Item


class ShieldPickup(Item):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "shields.png", PICKUP_SIZE)

    def apply_to(self, player):
        if player.hp >= player.max_hp:
            return False  # vida llena: se queda intacto en el suelo

        player.hp += 1
        return True
