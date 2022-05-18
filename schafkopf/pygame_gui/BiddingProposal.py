from typing import Union

import pygame
from pygame.font import Font

from schafkopf.game_modes import *
from schafkopf.pygame_gui.colors import WHITE, BLACK


class BiddingProposal(pygame.Surface):
    def __init__(self, player_passes: bool, width: int, height: int, font_size=40):
        super().__init__((width, height), pygame.SRCALPHA)
        self.set_alpha(180)
        pygame.draw.ellipse(self, WHITE, self.get_rect())
        self.font_size = font_size
        self._add_proposal(player_passes)

    def _add_proposal(self, player_passes: bool):
        text = self._get_proposal_text(player_passes)
        self.blit(text, self._get_text_position(text.get_width(), text.get_height()))

    def _get_proposal_text(self, player_passes):
        font = pygame.font.Font(None, self.font_size)
        if player_passes:
            text = "Weiter"
        else:
            text = "I dad spuin!"
        return font.render(text, True, BLACK)

    def _get_text_position(self, text_width, text_height):
        return self.get_width() // 2 - text_width // 2, self.get_height() // 2 - text_height // 2
