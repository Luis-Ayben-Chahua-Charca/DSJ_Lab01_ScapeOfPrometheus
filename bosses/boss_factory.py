from bosses.anubis import AnubisBoss
from bosses.apollo import ApolloBoss
from bosses.loki import LokiBoss

_BOSS_CLASSES = {
    "apollo": ApolloBoss,
    "anubis": AnubisBoss,
    "loki": LokiBoss,
}

# Tema musical por jefe (assets/music/), arranca en loop al entrar a boss_room.
BOSS_THEME_FILES = {
    "apollo": "orange_boss_theme.mp3",
    "anubis": "black_boss_theme.mp3",
    "loki": "green_boss_theme.mp3",
}


def create_boss(boss_id, screen, x, y):
    return _BOSS_CLASSES[boss_id](screen, x, y)
