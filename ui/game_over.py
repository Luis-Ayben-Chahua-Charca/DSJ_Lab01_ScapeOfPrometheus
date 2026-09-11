import pygame

from data.config import GAME_OVER_COLOR, GAME_OVER_FONT_SIZE, HINT_FONT_SIZE


class GameOverScreen:
    def __init__(self):
        self.font = pygame.font.Font("freesansbold.ttf", GAME_OVER_FONT_SIZE)
        self.hint_font = pygame.font.Font("freesansbold.ttf", HINT_FONT_SIZE)

    def draw(self, screen):
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        title = self.font.render("GAME OVER", True, GAME_OVER_COLOR)
        title_rect = title.get_rect(center=(center_x, center_y - 20))
        screen.blit(title, title_rect)

        hint = self.hint_font.render("R: reintentar   |   ESC: salir", True, GAME_OVER_COLOR)
        hint_rect = hint.get_rect(center=(center_x, title_rect.bottom + 40))
        screen.blit(hint, hint_rect)
