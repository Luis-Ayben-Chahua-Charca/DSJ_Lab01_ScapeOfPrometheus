import math

from data.config import COLLISION_DISTANCE


def is_collision(x1, y1, x2, y2):
    """Colisión bala-enemigo: distancia entre puntos (heredada del original)."""
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distance < COLLISION_DISTANCE


def rects_collide(entity_a, entity_b):
    """Colisión por rectángulo, usada para el contacto jugador-enemigo."""
    rect_a = entity_a.image.get_rect(topleft=(entity_a.x, entity_a.y))
    rect_b = entity_b.image.get_rect(topleft=(entity_b.x, entity_b.y))
    return rect_a.colliderect(rect_b)
