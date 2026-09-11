from pygame import mixer

from core.asset_loader import music_path
from data.config import MUSIC_TRANSITION_FADE_DURATION


class MusicManager:
    """Dueño del único canal de música en loop (mixer.music). Los jingles
    de una sola vez (victoria/derrota) no pasan por acá — se reproducen
    como Sound normales (core.asset_loader.load_sound), independientes de
    este canal."""

    def __init__(self):
        self._pending_path = None
        self._pending_delay = 0.0

    def play_immediately(self, filename):
        self._pending_path = None
        mixer.music.load(music_path(filename))
        mixer.music.play(-1)

    def switch_to(self, filename):
        """Atenúa la pista actual (fade-out corto) y, recién cuando termina,
        arranca la nueva en loop — evita el corte seco de reemplazar el
        stream a mitad de un fadeout en curso."""
        mixer.music.fadeout(int(MUSIC_TRANSITION_FADE_DURATION * 1000))
        self._pending_path = filename
        self._pending_delay = MUSIC_TRANSITION_FADE_DURATION

    def stop(self):
        self._pending_path = None
        mixer.music.stop()

    def tick(self, dt):
        if self._pending_path is None:
            return

        self._pending_delay -= dt
        if self._pending_delay <= 0:
            path, self._pending_path = self._pending_path, None
            mixer.music.load(music_path(path))
            mixer.music.play(-1)
