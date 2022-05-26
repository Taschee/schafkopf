from typing import Tuple

import pygame

from schafkopf.pygame_gui.Widget import Widget
from schafkopf.pygame_gui.colors import WHITE, BLACK

offset = 5


def _get_name_text(player_index: int, font_size: int):
    font = pygame.font.Font(None, font_size)
    return font.render(f'Spieler {player_index + 1}', True, BLACK)


def _get_score_text(score: int, font_size: int):
    font = pygame.font.Font(None, font_size)
    return font.render(f'{score / 100}0 €', True, BLACK)


class PlayerInfoWidget(Widget):
    def __init__(
        self,
        topleft: Tuple[int, int],
        player_index: int = 0,
        score: int = 0,
        font_size: int = 40,
        size: Tuple[int, int] = (210, 140)
    ):
        name_text = _get_name_text(player_index, font_size)
        score_text = _get_score_text(score, font_size)
        image = pygame.Surface(size, pygame.SRCALPHA)
        image.fill(WHITE)
        image.set_alpha(180)
        image.blit(name_text, (image.get_width() // 2 - name_text.get_width() // 2, offset))
        image.blit(score_text, (image.get_width() // 2 - score_text.get_width() // 2, 2 * offset + font_size))
        super().__init__(
            topleft=topleft,
            image=image
        )
