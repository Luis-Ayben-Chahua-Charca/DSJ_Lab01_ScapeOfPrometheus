import random

from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import COMBAT_ROOM_MAX_ENEMIES, COMBAT_ROOM_MIN_ENEMIES, ITEM_PICKUP_SIZE
from data.rooms_layout import ROOMS_LAYOUT
from items.registry import ITEM_CLASSES
from rooms.room import Room


class RoomManager:
    def __init__(self, screen, player, start_room_id="start"):
        self.screen = screen
        self.player = player
        self.start_room_id = start_room_id
        self.reset()

    def reset(self):
        """Reconstruye el mapa desde cero: salas sin limpiar, sin enemigos
        ni pickups, de vuelta en la sala inicial. Las salas de combate
        sortean una cantidad nueva de enemigos (2-6) cada vez. Usado al
        iniciar la run y al reintentar desde Game Over/Victoria."""
        self.rooms = {
            room_id: Room(
                room_id,
                data["grid_pos"],
                data["room_type"],
                data["connections"],
                self._roll_enemy_count(data["room_type"]),
            )
            for room_id, data in ROOMS_LAYOUT.items()
        }

        self.current_room_id = self.start_room_id
        self.visited = {self.start_room_id}

        self.current_room.ensure_spawned(self.screen, self.player)

    @staticmethod
    def _roll_enemy_count(room_type):
        if room_type != "combat":
            return 0
        return random.randint(COMBAT_ROOM_MIN_ENEMIES, COMBAT_ROOM_MAX_ENEMIES)

    @property
    def current_room(self):
        return self.rooms[self.current_room_id]

    def enter_room(self, room_id):
        self.current_room_id = room_id
        self.visited.add(room_id)

        room = self.current_room
        if room.room_type == "item":
            self._ensure_item_spawned(room)
        else:
            room.ensure_spawned(self.screen, self.player)

    def _ensure_item_spawned(self, room):
        """Sala de ítem: sin dado de probabilidad, siempre da un ítem al
        azar en el centro la primera vez que se entra."""
        if room.spawned:
            return

        room.spawned = True

        item_cls = random.choice(ITEM_CLASSES)
        x = SCREEN_WIDTH / 2 - ITEM_PICKUP_SIZE / 2
        y = SCREEN_HEIGHT / 2 - ITEM_PICKUP_SIZE / 2
        room.add_pickup(item_cls(self.screen, x, y))

    def discovered_room_ids(self):
        """Salas visitadas + sus vecinas directas (descubiertas pero no exploradas)."""
        discovered = set(self.visited)

        for room_id in self.visited:
            for neighbor_id in self.rooms[room_id].connections.values():
                if neighbor_id:
                    discovered.add(neighbor_id)

        return discovered
