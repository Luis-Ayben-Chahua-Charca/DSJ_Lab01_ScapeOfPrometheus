import pygame

from core.constants import SCREEN_WIDTH
from data.config import (
    MINIMAP_BORDER_COLOR,
    MINIMAP_CELL_SIZE,
    MINIMAP_CURRENT_COLOR,
    MINIMAP_DISCOVERED_COLOR,
    MINIMAP_GAP,
    MINIMAP_MARGIN,
    MINIMAP_VISITED_COLOR,
)


class Minimap:
    def draw(self, screen, room_manager):
        discovered = room_manager.discovered_room_ids()
        rooms = room_manager.rooms.values()

        # Tamaño del grid derivado de las coordenadas reales del mapa, en vez
        # de un span fijo: se adapta solo a mapas más grandes/irregulares.
        cols = [room.grid_pos[0] for room in rooms]
        rows = [room.grid_pos[1] for room in rooms]
        min_col, max_col = min(cols), max(cols)
        min_row = min(rows)

        cell_step = MINIMAP_CELL_SIZE + MINIMAP_GAP
        grid_width = (max_col - min_col + 1) * cell_step - MINIMAP_GAP

        origin_x = SCREEN_WIDTH - MINIMAP_MARGIN - grid_width
        origin_y = MINIMAP_MARGIN

        for room_id, room in room_manager.rooms.items():
            if room_id not in discovered:
                continue

            col = room.grid_pos[0] - min_col
            row = room.grid_pos[1] - min_row

            rect = pygame.Rect(
                origin_x + col * cell_step,
                origin_y + row * cell_step,
                MINIMAP_CELL_SIZE,
                MINIMAP_CELL_SIZE,
            )

            if room_id == room_manager.current_room_id:
                color = MINIMAP_CURRENT_COLOR
            elif room_id in room_manager.visited:
                color = MINIMAP_VISITED_COLOR
            else:
                color = MINIMAP_DISCOVERED_COLOR

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, MINIMAP_BORDER_COLOR, rect, 1)
