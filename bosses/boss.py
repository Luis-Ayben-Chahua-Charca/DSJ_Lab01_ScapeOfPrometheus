import pygame

from core.asset_loader import load_image
from data.config import BOSS_FADE_DURATION, BOSS_MAX_HP, BOSS_SIZE
from entities.entity import Entity


def compute_fade_alpha(elapsed, duration, fading_in=True):
    """Progreso lineal de alpha (0-255) de un fade-in o fade-out de la
    duración dada. Compartido por el fade-in de entrada de todos los jefes
    y por el teletransporte de Loki (fade-out + fade-in), en vez de que
    cada uno repita la misma cuenta."""
    if duration <= 0:
        return 255 if fading_in else 0

    ratio = min(1.0, max(0.0, elapsed / duration))
    return int(255 * ratio) if fading_in else int(255 * (1 - ratio))


class Boss(Entity):
    """Base compartida por los 3 jefes. Cada subclase implementa su propio
    patrón de comportamiento en update()."""

    def __init__(self, screen, name, image_filename, x, y):
        image = pygame.transform.smoothscale(load_image(image_filename), (BOSS_SIZE, BOSS_SIZE))
        super().__init__(screen, image, x, y)

        self.name = name
        self.max_hp = BOSS_MAX_HP
        self.hp = BOSS_MAX_HP
        self.spawn_time = 0.0

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def fade_alpha(self):
        return compute_fade_alpha(self.spawn_time, BOSS_FADE_DURATION, fading_in=True)

    def tick_spawn_fade(self, dt):
        if self.spawn_time < BOSS_FADE_DURATION:
            self.spawn_time += dt

    def take_bullet_hit(self):
        self.hp = max(0, self.hp - 1)

    def update(self, dt, player):
        """Actualiza el comportamiento del jefe. Devuelve una lista de
        proyectiles nuevos disparados este frame (vacía si no dispara)."""
        raise NotImplementedError

    def get_beam_rect(self):
        """pygame.Rect de un rayo activo dañando por superposición, o None
        si el jefe no usa ese mecanismo (solo Anubis lo sobreescribe)."""
        return None

    def draw(self):
        self.image.set_alpha(self.fade_alpha)
        self.screen.blit(self.image, (self.x, self.y))
