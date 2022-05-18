from typing import Union

import pygame
from pygame.font import Font

from schafkopf.game_modes import *


class BiddingOption(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), option=(NO_GAME, None), font_size=40):
        pygame.sprite.Sprite.__init__(self)
        self.option = option
        self.font_size = font_size
        self.image = Font(None, font_size).render(
            get_bidding_option_as_text(self.option), True, pygame.Color('black'), pygame.Color('white')
        )
        self.rect = self.image.get_rect(topleft=pos)


def get_bidding_option_as_text(option: tuple[int, Union[int, None]]):
    if option[1] is None:
        return game_mode_dict[option[0]]
    else:
        return game_mode_dict[option[0]] + " " + suit_dict[option[1]]


game_mode_dict: dict[int, str] = {
    NO_GAME: "Weiter",
    PARTNER_MODE: "Sauspiel",
    WENZ: "Wenz",
    SOLO: "Solo",
}

suit_dict: dict[int, str] = {
    ACORNS: "Eichel",
    LEAVES: "Gras",
    HEARTS: "Herz",
    BELLS: "Schellen"
}
