import pygame

from bosses.boss import Boss
from core.constants import SCREEN_HEIGHT
from data.config import (
    ANUBIS_ALIGN_SPEED,
    ANUBIS_BEAM_COLOR,
    ANUBIS_BEAM_DURATION,
    ANUBIS_BEAM_PAUSE,
    ANUBIS_BEAM_THICKNESS,
    ANUBIS_TELEGRAPH_ALPHA,
    ANUBIS_TELEGRAPH_DURATION,
    ANUBIS_TELEGRAPH_THICKNESS,
    ANUBIS_Y_OFFSET,
    BOSS_MAX_X,
    BOSS_MIN_X,
    BOSS_MIN_Y,
    BOSS_SIZE,
    PLAYER_SIZE,
    WALL_THICKNESS,
)

STATE_ALIGN = "align"
STATE_TELEGRAPH = "telegraph"
STATE_BEAM = "beam"
STATE_PAUSE = "pause"


class AnubisBoss(Boss):
    """No persigue al jugador: se alinea en X manteniéndose arriba, avisa
    con una línea delgada (telegraph, sin daño) y recién después dispara el
    rayo continuo real hacia abajo por esa columna."""

    def __init__(self, screen, x, y):
        super().__init__(screen, "Anubis", "Black_boss.png", x, y)
        self.y = BOSS_MIN_Y + ANUBIS_Y_OFFSET
        self.state = STATE_ALIGN
        self.state_timer = 0.0

    def update(self, dt, player):
        self.tick_spawn_fade(dt)

        if self.state == STATE_ALIGN:
            self._align_with(player)

            if self._is_aligned(player):
                self.state = STATE_TELEGRAPH
                self.state_timer = 0.0

        elif self.state == STATE_TELEGRAPH:
            self.state_timer += dt

            if self.state_timer >= ANUBIS_TELEGRAPH_DURATION:
                self.state = STATE_BEAM
                self.state_timer = 0.0

        elif self.state == STATE_BEAM:
            self.state_timer += dt

            if self.state_timer >= ANUBIS_BEAM_DURATION:
                self.state = STATE_PAUSE
                self.state_timer = 0.0

        elif self.state == STATE_PAUSE:
            self.state_timer += dt

            if self.state_timer >= ANUBIS_BEAM_PAUSE:
                self.state = STATE_ALIGN

        return []

    def _target_x(self, player):
        return player.x + PLAYER_SIZE / 2 - BOSS_SIZE / 2

    def _align_with(self, player):
        target_x = self._target_x(player)
        dx = target_x - self.x

        if abs(dx) > ANUBIS_ALIGN_SPEED:
            self.x += ANUBIS_ALIGN_SPEED if dx > 0 else -ANUBIS_ALIGN_SPEED
        else:
            self.x = target_x

        if self.x < BOSS_MIN_X:
            self.x = BOSS_MIN_X
        elif self.x > BOSS_MAX_X:
            self.x = BOSS_MAX_X

    def _is_aligned(self, player):
        return abs(self.x - self._target_x(player)) <= ANUBIS_ALIGN_SPEED

    def _trajectory_rect(self, thickness):
        beam_x = self.x + BOSS_SIZE / 2 - thickness / 2
        beam_y = self.y + BOSS_SIZE
        beam_height = (SCREEN_HEIGHT - WALL_THICKNESS) - beam_y

        return pygame.Rect(beam_x, beam_y, thickness, beam_height)

    def get_beam_rect(self):
        """Solo el rayo REAL (con daño). El telegraph es puramente visual,
        por eso no se expone acá."""
        if self.state != STATE_BEAM:
            return None

        return self._trajectory_rect(ANUBIS_BEAM_THICKNESS)

    def _get_telegraph_rect(self):
        if self.state != STATE_TELEGRAPH:
            return None

        return self._trajectory_rect(ANUBIS_TELEGRAPH_THICKNESS)

    def draw(self):
        super().draw()

        telegraph_rect = self._get_telegraph_rect()
        if telegraph_rect is not None:
            # Línea delgada y semitransparente: misma trayectoria que el
            # rayo real, pero de advertencia, sin dañar.
            telegraph_surface = pygame.Surface((telegraph_rect.width, telegraph_rect.height), pygame.SRCALPHA)
            telegraph_surface.fill((*ANUBIS_BEAM_COLOR, ANUBIS_TELEGRAPH_ALPHA))
            self.screen.blit(telegraph_surface, telegraph_rect.topleft)
            return

        beam_rect = self.get_beam_rect()
        if beam_rect is None:
            return

        # Brillo semitransparente detrás, un poco más ancho que el rayo.
        glow_rect = beam_rect.inflate(ANUBIS_BEAM_THICKNESS, 0)
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        glow_surface.fill((*ANUBIS_BEAM_COLOR, 60))
        self.screen.blit(glow_surface, glow_rect.topleft)

        pygame.draw.rect(self.screen, ANUBIS_BEAM_COLOR, beam_rect)
