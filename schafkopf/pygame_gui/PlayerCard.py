from typing import Tuple, Callable

import pygame

from schafkopf.pygame_gui.Button import Button
from schafkopf.ranks import SEVEN, EIGHT, TEN, NINE, UNTER, OBER, KING, ACE
from schafkopf.suits import ACORNS, LEAVES, HEARTS, BELLS


class PlayerCard(Button):
    def __init__(
        self,
        topleft: Tuple[int, int],
        card_encoded: Tuple[int, int],
        callback: Callable = None,
        hover_effect: bool = True
    ):
        self.card_encoded = card_encoded
        pic_name = self._get_card_image_name(card_encoded)
        self.image = pygame.image.load(pic_name).convert()
        self.image.set_alpha(200)
        self.hover_image = pygame.image.load(pic_name).convert()
        if hover_effect:
            self.hover_image.set_alpha(None)
        super().__init__(
            topleft=topleft,
            image=self.image,
            button_down_image=self.image,
            hover_image=self.hover_image,
            callback=callback
        )

    @staticmethod
    def _get_card_image_name(encoded_card):
        return "../images/" + rank_dict[encoded_card[0]] + suit_dict[encoded_card[1]] + ".jpg"


rank_dict: dict[int, str] = {
    SEVEN: "7",
    EIGHT: "8",
    NINE: "9",
    TEN: "10",
    UNTER: "U",
    OBER: "O",
    KING: "K",
    ACE: "A",
}

suit_dict: dict[int, str] = {
    ACORNS: "Eichel",
    LEAVES: "Gras",
    HEARTS: "Herz",
    BELLS: "Schellen"
}
