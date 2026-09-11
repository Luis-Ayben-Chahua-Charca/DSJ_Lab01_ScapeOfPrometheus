# Mapa fijo de 9 salas. Coordenadas de grilla (columna, fila), fila creciendo
# hacia abajo, start en (0,0):
#
#                     [north] (0,-1)
#                         |
# [item_room] (-1,1)      |
#       |               [start] (0,0) — [east1] — [east2] — [east3]
#     [west] (-1,0) ——————/                                     |
#                         |                                 [corridor] (3,-1)
#                     [south] (0,1)                              |
#                                                          [boss_room] (3,-2)
#
# "connections" indica, para cada lado (N/S/E/W), el id de la sala vecina;
# los lados sin puerta simplemente no tienen esa clave (pared llena).
#
# room_type: "start" (spawn, sin combate, ya limpia), "combat" (enemigos
# 2-6 sorteados en RoomManager.reset()), "item" (sin combate, da un ítem
# garantizado al entrar), "boss" (placeholder — fase del jefe todavía no
# implementada).

ROOMS_LAYOUT = {
    "start": {
        "grid_pos": (0, 0),
        "room_type": "start",
        "connections": {"N": "north", "S": "south", "E": "east1", "W": "west"},
    },
    "north": {
        "grid_pos": (0, -1),
        "room_type": "combat",
        "connections": {"S": "start"},
    },
    "south": {
        "grid_pos": (0, 1),
        "room_type": "combat",
        "connections": {"N": "start"},
    },
    "west": {
        "grid_pos": (-1, 0),
        "room_type": "combat",
        "connections": {"E": "start", "S": "item_room"},
    },
    "item_room": {
        "grid_pos": (-1, 1),
        "room_type": "item",
        "connections": {"N": "west"},
    },
    "east1": {
        "grid_pos": (1, 0),
        "room_type": "combat",
        "connections": {"W": "start", "E": "east2"},
    },
    "east2": {
        "grid_pos": (2, 0),
        "room_type": "combat",
        "connections": {"W": "east1", "E": "east3"},
    },
    "east3": {
        "grid_pos": (3, 0),
        "room_type": "combat",
        "connections": {"W": "east2", "N": "corridor"},
    },
    "corridor": {
        "grid_pos": (3, -1),
        "room_type": "combat",
        "connections": {"S": "east3", "N": "boss_room"},
    },
    "boss_room": {
        "grid_pos": (3, -2),
        "room_type": "boss",
        "connections": {"S": "corridor"},
    },
}
