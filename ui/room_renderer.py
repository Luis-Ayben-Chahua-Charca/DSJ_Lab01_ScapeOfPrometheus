import pygame

from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import DOOR_BAND_X, DOOR_BAND_Y, DOOR_CLOSED_COLOR, DOOR_MARK_COLOR, WALL_COLOR, WALL_THICKNESS


def draw_room(screen, room):
    _draw_side(screen, room, "N")
    _draw_side(screen, room, "S")
    _draw_side(screen, room, "E")
    _draw_side(screen, room, "W")


def _draw_side(screen, room, direction):
    has_door = room.connections.get(direction) is not None
    door_open = has_door and room.is_clear

    if direction in ("N", "S"):
        y = 0 if direction == "N" else SCREEN_HEIGHT - WALL_THICKNESS
        door_min, door_max = DOOR_BAND_X

        if not has_door:
            pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, y, SCREEN_WIDTH, WALL_THICKNESS))
            return

        pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, y, door_min, WALL_THICKNESS))
        pygame.draw.rect(
            screen, WALL_COLOR, pygame.Rect(door_max, y, SCREEN_WIDTH - door_max, WALL_THICKNESS)
        )
        gap_rect = pygame.Rect(door_min, y, door_max - door_min, WALL_THICKNESS)
    else:
        x = 0 if direction == "W" else SCREEN_WIDTH - WALL_THICKNESS
        door_min, door_max = DOOR_BAND_Y

        if not has_door:
            pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(x, 0, WALL_THICKNESS, SCREEN_HEIGHT))
            return

        pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(x, 0, WALL_THICKNESS, door_min))
        pygame.draw.rect(
            screen, WALL_COLOR, pygame.Rect(x, door_max, WALL_THICKNESS, SCREEN_HEIGHT - door_max)
        )
        gap_rect = pygame.Rect(x, door_min, WALL_THICKNESS, door_max - door_min)

    if not door_open:
        pygame.draw.rect(screen, DOOR_CLOSED_COLOR, gap_rect)
        pygame.draw.line(screen, DOOR_MARK_COLOR, gap_rect.topleft, gap_rect.bottomright, 4)
        pygame.draw.line(screen, DOOR_MARK_COLOR, gap_rect.topright, gap_rect.bottomleft, 4)
    # Puerta abierta: se deja el hueco sin pintar (se ve el fondo detrás), como paso libre.
