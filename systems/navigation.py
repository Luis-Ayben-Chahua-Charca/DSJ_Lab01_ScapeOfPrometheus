from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import (
    DOOR_BAND_X,
    DOOR_BAND_Y,
    PLAYER_MAX_X,
    PLAYER_MAX_Y,
    PLAYER_MIN_X,
    PLAYER_MIN_Y,
    PLAYER_SIZE,
)


def update_room_transitions(player, room_manager):
    """Bloquea al jugador contra paredes/puertas cerradas, y lo cruza a la
    sala vecina en cuanto atraviesa una puerta abierta."""

    room = room_manager.current_room
    door_open = room.is_clear

    center_x = player.x + PLAYER_SIZE / 2
    center_y = player.y + PLAYER_SIZE / 2
    x_in_door_band = DOOR_BAND_X[0] <= center_x <= DOOR_BAND_X[1]
    y_in_door_band = DOOR_BAND_Y[0] <= center_y <= DOOR_BAND_Y[1]

    if player.y < PLAYER_MIN_Y:
        target = room.connections.get("N")
        if door_open and target and x_in_door_band:
            _enter_room(player, room_manager, target, entered_from="N")
        else:
            player.y = PLAYER_MIN_Y
    elif player.y > PLAYER_MAX_Y:
        target = room.connections.get("S")
        if door_open and target and x_in_door_band:
            _enter_room(player, room_manager, target, entered_from="S")
        else:
            player.y = PLAYER_MAX_Y

    if player.x < PLAYER_MIN_X:
        target = room.connections.get("W")
        if door_open and target and y_in_door_band:
            _enter_room(player, room_manager, target, entered_from="W")
        else:
            player.x = PLAYER_MIN_X
    elif player.x > PLAYER_MAX_X:
        target = room.connections.get("E")
        if door_open and target and y_in_door_band:
            _enter_room(player, room_manager, target, entered_from="E")
        else:
            player.x = PLAYER_MAX_X


def _enter_room(player, room_manager, target_room_id, entered_from):
    mid_x = SCREEN_WIDTH / 2 - PLAYER_SIZE / 2
    mid_y = SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2

    # Reaparece cerca del borde opuesto al que cruzó (ej: salió por la
    # puerta norte -> entra pegado al borde sur de la sala vecina). Esto se
    # hace ANTES de avisarle a room_manager para que, si la sala vecina
    # spawnea enemigos recién ahora, la exclusión de spawn cerca del
    # jugador (ver systems/spawn.py) use la posición ya correcta.
    if entered_from == "N":
        player.x, player.y = mid_x, PLAYER_MAX_Y - 4
    elif entered_from == "S":
        player.x, player.y = mid_x, PLAYER_MIN_Y + 4
    elif entered_from == "W":
        player.x, player.y = PLAYER_MAX_X - 4, mid_y
    elif entered_from == "E":
        player.x, player.y = PLAYER_MIN_X + 4, mid_y

    room_manager.enter_room(target_room_id)
