import pygame

from schafkopf.pygame_gui.colors import WHITE, BLACK


class PlayerName(pygame.Surface):
    def __init__(self, player_index: int, font_size=40):
        self.font_size = font_size
        text = self._get_name_text(player_index)
        super().__init__(text.get_rect().size, pygame.SRCALPHA)
        self.set_alpha(180)
        self.fill(WHITE)
        self._add_name(text)

    def _add_name(self, text):
        self.blit(text, self._get_text_position(text.get_width(), text.get_height()))

    def _get_name_text(self, player_index):
        font = pygame.font.Font(None, self.font_size)
        return font.render(f'Spieler {player_index + 1}', True, BLACK)

    def _get_text_position(self, text_width, text_height):
        return self.get_width() // 2 - text_width // 2, self.get_height() // 2 - text_height // 2
