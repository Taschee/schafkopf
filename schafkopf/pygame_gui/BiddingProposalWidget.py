from typing import Tuple

import pygame

from schafkopf.pygame_gui.Widget import Widget
from schafkopf.pygame_gui.colors import WHITE, BLACK


class BiddingProposalWidget(Widget):
    def __init__(
        self,
        topleft: Tuple[int, int],
        player_passes: bool,
        width: int,
        height: int,
        font_size=40
    ):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, WHITE, self.image.get_rect())
        self.image.set_alpha(180)
        self.font_size = font_size
        self._add_proposal(player_passes)
        super().__init__(topleft=topleft, image=self.image)

    def _add_proposal(self, player_passes: bool):
        text = self._get_proposal_text(player_passes)
        self.image.blit(text, self._get_text_position(text.get_width(), text.get_height()))

    def _get_proposal_text(self, player_passes: bool):
        font = pygame.font.Font(None, self.font_size)
        if player_passes:
            text = "Weiter"
        else:
            text = "I dad spuin!"
        return font.render(text, True, BLACK)

    def _get_text_position(self, text_width, text_height):
        return self.image.get_width() // 2 - text_width // 2, self.image.get_height() // 2 - text_height // 2
