import pygame

from core.asset_loader import load_image
from data.config import (
    SCORE_COLOR,
    SCORE_FONT_SIZE,
    SCORE_TEXT_POS,
    SHIELD_ICON_EMPTY_ALPHA,
    SHIELD_ICON_GAP,
    SHIELD_ICON_POS,
    SHIELD_ICON_SIZE,
)


class HUD:
    def __init__(self):
        self.font = pygame.font.Font("freesansbold.ttf", SCORE_FONT_SIZE)

        icon = pygame.transform.smoothscale(
            load_image("shields.png").convert_alpha(), (SHIELD_ICON_SIZE, SHIELD_ICON_SIZE)
        )
        self.shield_icon_full = icon
        self.shield_icon_empty = icon.copy()
        self.shield_icon_empty.set_alpha(SHIELD_ICON_EMPTY_ALPHA)

    def show_hp(self, screen, player, pos=SHIELD_ICON_POS):
        """Dibuja player.max_hp escudos: los primeros player.hp llenos, el resto atenuados."""
        x, y = pos

        for i in range(player.max_hp):
            icon = self.shield_icon_full if i < player.hp else self.shield_icon_empty
            icon_x = x + i * (SHIELD_ICON_SIZE + SHIELD_ICON_GAP)
            screen.blit(icon, (icon_x, y))

    def show_score(self, screen, score_value, pos=SCORE_TEXT_POS):
        score_surface = self.font.render(f"Score : {score_value}", True, SCORE_COLOR)
        screen.blit(score_surface, pos)
