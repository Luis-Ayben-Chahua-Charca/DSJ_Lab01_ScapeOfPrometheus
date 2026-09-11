import random

_ALL_BOSSES = ["apollo", "anubis", "loki"]

# Bolsa a nivel de módulo: persiste mientras el proceso siga corriendo, entre
# reintentos con R. Deliberadamente independiente del ciclo de vida de una
# run: no se resetea en RoomManager.reset() ni en Player.reset().
_bag = []


def draw_next_boss():
    global _bag

    if not _bag:
        _bag = list(_ALL_BOSSES)
        random.shuffle(_bag)

    return _bag.pop()
