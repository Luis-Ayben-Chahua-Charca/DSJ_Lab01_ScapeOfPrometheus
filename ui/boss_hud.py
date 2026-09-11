import pygame

from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.config import (
    BOSS_HP_BAR_BG_COLOR,
    BOSS_HP_BAR_BORDER_COLOR,
    BOSS_HP_BAR_COLOR,
    BOSS_HP_BAR_HEIGHT,
    BOSS_HP_BAR_MARGIN_BOTTOM,
    BOSS_HP_BAR_WIDTH,
    BOSS_NAME_COLOR,
    BOSS_NAME_FONT_SIZE,
    BOSS_NAME_Y,
)


class BossHUD:
    def __init__(self):
        self.font = pygame.font.Font("freesansbold.ttf", BOSS_NAME_FONT_SIZE)

    def draw(self, screen, boss):
        name_surface = self.font.render(boss.name, True, BOSS_NAME_COLOR)
        name_surface.set_alpha(boss.fade_alpha)
        name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, BOSS_NAME_Y))
        screen.blit(name_surface, name_rect)

        bar_x = SCREEN_WIDTH // 2 - BOSS_HP_BAR_WIDTH // 2
        bar_y = SCREEN_HEIGHT - BOSS_HP_BAR_MARGIN_BOTTOM - BOSS_HP_BAR_HEIGHT

        bg_rect = pygame.Rect(bar_x, bar_y, BOSS_HP_BAR_WIDTH, BOSS_HP_BAR_HEIGHT)
        pygame.draw.rect(screen, BOSS_HP_BAR_BG_COLOR, bg_rect)

        ratio = max(0, boss.hp) / boss.max_hp
        fill_rect = pygame.Rect(bar_x, bar_y, int(BOSS_HP_BAR_WIDTH * ratio), BOSS_HP_BAR_HEIGHT)
        pygame.draw.rect(screen, BOSS_HP_BAR_COLOR, fill_rect)

        pygame.draw.rect(screen, BOSS_HP_BAR_BORDER_COLOR, bg_rect, 2)
