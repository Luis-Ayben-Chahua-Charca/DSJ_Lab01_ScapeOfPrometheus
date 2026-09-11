import pygame

from core.asset_loader import load_image
from core.constants import SCREEN_HEIGHT
from data.config import (
    ITEM_HUD_BADGE_COLOR,
    ITEM_HUD_BADGE_FONT_SIZE,
    ITEM_HUD_BADGE_TEXT_COLOR,
    ITEM_HUD_ICON_GAP,
    ITEM_HUD_ICON_SIZE,
    ITEM_HUD_MARGIN,
)

# (clave interna, archivo de sprite, atributo de conteo en Player o None si
# es on/off). Mismo orden en el que se dibujan de izquierda a derecha.
_ITEM_ENTRIES = [
    ("telescope", "telescopio.png", "telescope_count"),
    ("probe", "sonda.png", "speed_item_count"),
    ("asteroid", "asteroide.png", None),  # flag on/off (player.pierces)
    ("satellite", "satelite.png", "satellite_count"),
    ("astronaut", "astronauta.png", "astronaut_count"),
]


class ItemHUD:
    """Fila de íconos de los ítems que el jugador ya recogió, abajo a la
    izquierda (no choca con escudos/score arriba-izquierda, el minimapa
    arriba-derecha, ni la barra de vida del jefe abajo-centro)."""

    def __init__(self):
        self.badge_font = pygame.font.Font("freesansbold.ttf", ITEM_HUD_BADGE_FONT_SIZE)
        self.icons = {
            key: pygame.transform.smoothscale(load_image(filename), (ITEM_HUD_ICON_SIZE, ITEM_HUD_ICON_SIZE))
            for key, filename, _ in _ITEM_ENTRIES
        }

    def draw(self, screen, player):
        x = ITEM_HUD_MARGIN
        y = SCREEN_HEIGHT - ITEM_HUD_MARGIN - ITEM_HUD_ICON_SIZE

        for key, _, count_attr in _ITEM_ENTRIES:
            if count_attr is None:
                owned, count = player.pierces, None
            else:
                count = getattr(player, count_attr)
                owned = count > 0

            if not owned:
                continue

            screen.blit(self.icons[key], (x, y))

            if count is not None and count > 1:
                self._draw_badge(screen, count, x, y)

            x += ITEM_HUD_ICON_SIZE + ITEM_HUD_ICON_GAP

    def _draw_badge(self, screen, count, icon_x, icon_y):
        text = self.badge_font.render(str(count), True, ITEM_HUD_BADGE_TEXT_COLOR)
        badge_rect = text.get_rect().inflate(6, 4)
        badge_rect.bottomright = (icon_x + ITEM_HUD_ICON_SIZE, icon_y + ITEM_HUD_ICON_SIZE)

        pygame.draw.rect(screen, ITEM_HUD_BADGE_COLOR, badge_rect, border_radius=4)
        screen.blit(text, text.get_rect(center=badge_rect.center))
