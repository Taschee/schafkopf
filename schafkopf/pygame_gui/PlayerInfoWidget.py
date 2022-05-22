import pygame

from schafkopf.pygame_gui.colors import WHITE, BLACK

offset = 5


class PlayerInfoWidget(pygame.Surface):
    def __init__(self, player_index: int = 0, score: int = 0, font_size: int = 40):
        self.font_size = font_size
        name_text = self._get_name_text(player_index)
        score_text = self._get_score_text(score)
        super().__init__((name_text.get_width() + 2 * offset, 3 * name_text.get_height() + 2 * offset), pygame.SRCALPHA)
        self.fill(WHITE)
        self.set_alpha(180)
        self._add_name(name_text)
        self._add_score(score_text)

    def _add_name(self, text):
        self.blit(text, self._get_text_position(text.get_width()))

    def _get_name_text(self, player_index: int):
        font = pygame.font.Font(None, self.font_size)
        return font.render(f'Spieler {player_index + 1}', True, BLACK)

    def _get_text_position(self, text_width: int):
        return self.get_width() // 2 - text_width // 2, offset

    def _get_score_text(self, score: int):
        font = pygame.font.Font(None, self.font_size)
        return font.render(f'{score / 100} €', True, BLACK)

    def _add_score(self, score_text):
        self.blit(score_text, self._get_score_position(score_text.get_width()))

    def _get_score_position(self, score_width):
        return self.get_width() // 2 - score_width // 2, 2 * offset + self.font_size
