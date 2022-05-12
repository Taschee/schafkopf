import pygame

from schafkopf.game_modes import *

BUTTON_UP_IMG = pygame.Surface((50, 30))
BUTTON_UP_IMG.fill('dodgerblue2')


class BiddingOption(pygame.sprite.Sprite):
    def __init__(self, pos, option):
        pygame.sprite.Sprite.__init__(self)
        font = pygame.font.Font(None, 30)
        self.image = font.render(
            self._get_bidding_option_as_text(option), True, pygame.Color('gray12'), (255, 255, 255)
        )
        self.rect = self.image.get_rect(topleft=pos)

    @staticmethod
    def _get_bidding_option_as_text(option):
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
