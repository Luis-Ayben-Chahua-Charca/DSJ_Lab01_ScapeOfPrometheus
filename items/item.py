import pygame

from core.asset_loader import load_image
from entities.entity import Entity


class Item(Entity):
    """Clase base para cualquier pickup del suelo (escudo o ítem real).
    Cachea el ícono escalado por (archivo, tamaño) para no releer/reescalar
    la imagen en cada drop."""

    _icon_cache = {}

    def __init__(self, screen, x, y, image_filename, size):
        super().__init__(screen, self._get_icon(image_filename, size), x, y)

    @classmethod
    def _get_icon(cls, image_filename, size):
        key = (image_filename, size)

        if key not in cls._icon_cache:
            cls._icon_cache[key] = pygame.transform.smoothscale(load_image(image_filename), (size, size))

        return cls._icon_cache[key]

    def apply_to(self, player):
        """Aplica el efecto y devuelve True si el pickup debe consumirse.
        Devolver False (ej. escudo con vida llena) lo deja intacto en el suelo."""
        raise NotImplementedError
