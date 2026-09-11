from data.config import ITEM_PICKUP_SIZE, TELESCOPE_COOLDOWN_MULTIPLIER
from items.item import Item


class TelescopePickup(Item):
    """Duplica la cadencia de disparo: cada copia multiplica el cooldown efectivo por 0.5."""

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "telescopio.png", ITEM_PICKUP_SIZE)

    def apply_to(self, player):
        player.fire_cooldown_multiplier *= TELESCOPE_COOLDOWN_MULTIPLIER
        player.telescope_count += 1
        return True
