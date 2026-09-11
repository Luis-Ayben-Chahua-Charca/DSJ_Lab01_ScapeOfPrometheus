from bosses.anubis import AnubisBoss
from bosses.apollo import ApolloBoss
from bosses.loki import LokiBoss

_BOSS_CLASSES = {
    "apollo": ApolloBoss,
    "anubis": AnubisBoss,
    "loki": LokiBoss,
}


def create_boss(boss_id, screen, x, y):
    return _BOSS_CLASSES[boss_id](screen, x, y)
