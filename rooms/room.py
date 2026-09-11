from systems.spawn import spawn_enemies


class Room:
    def __init__(self, room_id, grid_pos, room_type, connections=None, enemy_count=0):
        self.room_id = room_id
        self.grid_pos = grid_pos
        self.room_type = room_type
        self.connections = connections or {}
        self.enemy_count = enemy_count

        self.enemies = []
        self.pickups = []
        self.spawned = False
        self.is_clear = enemy_count == 0

    def ensure_spawned(self, screen, player=None):
        if self.spawned:
            return

        self.spawned = True

        if self.enemy_count > 0:
            self.enemies = spawn_enemies(screen, self.enemy_count, player)

    def kill_enemy(self, enemy):
        self.enemies.remove(enemy)

        if not self.enemies:
            self.is_clear = True

    def add_pickup(self, pickup):
        self.pickups.append(pickup)

    def remove_pickup(self, pickup):
        self.pickups.remove(pickup)
