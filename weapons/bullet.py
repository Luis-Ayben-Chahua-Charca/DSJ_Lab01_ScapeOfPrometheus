import pygame

from core.asset_loader import load_image, load_sound
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import BULLET_SPEED, PLAYER_SIZE

OFFSCREEN_MARGIN = 40

_vertical_image = None
_horizontal_image = None


def _get_images():
    global _vertical_image, _horizontal_image

    if _vertical_image is None:
        # El sprite viene orientado para tiro vertical; para izquierda/derecha
        # se usa una copia rotada 90° en vez de deformar el original.
        _vertical_image = load_image("bullet.png")
        _horizontal_image = pygame.transform.rotate(_vertical_image, 90)

    return _vertical_image, _horizontal_image


class Bullet:
    """Una bala activa e independiente. El jugador puede tener varias en
    pantalla a la vez (una por disparo, ya no hay estado ready/fire)."""

    def __init__(self, screen, player, direction, pierces=False):
        self.screen = screen

        dx, dy = direction
        vertical_image, horizontal_image = _get_images()
        self.image = horizontal_image if dx != 0 else vertical_image

        self.direction = direction
        self.pierces = pierces
        self.x, self.y = self._origin(player, dx, dy)

        load_sound("laser.wav").play()

    def _origin(self, player, dx, dy):
        """Punto de salida desde el borde de la nave correspondiente a la dirección disparada."""
        width, height = self.image.get_size()
        center_x = player.x + PLAYER_SIZE / 2
        center_y = player.y + PLAYER_SIZE / 2

        if dx == 1:
            return player.x + PLAYER_SIZE, center_y - height / 2
        if dx == -1:
            return player.x - width, center_y - height / 2
        if dy == -1:
            return center_x - width / 2, player.y - height

        return center_x - width / 2, player.y + PLAYER_SIZE

    def update(self):
        self.x += self.direction[0] * BULLET_SPEED
        self.y += self.direction[1] * BULLET_SPEED

    def is_off_screen(self):
        return (
            self.x < -OFFSCREEN_MARGIN
            or self.x > SCREEN_WIDTH + OFFSCREEN_MARGIN
            or self.y < -OFFSCREEN_MARGIN
            or self.y > SCREEN_HEIGHT + OFFSCREEN_MARGIN
        )

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
