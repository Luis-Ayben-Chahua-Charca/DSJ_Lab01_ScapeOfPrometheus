import pygame

from core.asset_loader import load_image
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import PLASMA_BALL_SIZE

OFFSCREEN_MARGIN = 60

_image = None


def _get_image():
    global _image

    if _image is None:
        _image = pygame.transform.smoothscale(load_image("plasma_ball.png"), (PLASMA_BALL_SIZE, PLASMA_BALL_SIZE))

    return _image


class BossProjectile:
    """Proyectil genérico de jefe (Apolo y Loki comparten esta clase y el
    sprite plasma_ball). Se mueve en línea recta en una dirección fija."""

    def __init__(self, screen, center_x, center_y, direction, speed):
        self.screen = screen
        self.image = _get_image()
        self.x = center_x - self.image.get_width() / 2
        self.y = center_y - self.image.get_height() / 2
        self.direction = direction
        self.speed = speed

    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def is_off_screen(self):
        return (
            self.x < -OFFSCREEN_MARGIN
            or self.x > SCREEN_WIDTH + OFFSCREEN_MARGIN
            or self.y < -OFFSCREEN_MARGIN
            or self.y > SCREEN_HEIGHT + OFFSCREEN_MARGIN
        )

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
