import pygame

from schafkopf.ranks import *
from schafkopf.suits import *


class Card(pygame.sprite.Sprite):
    def __init__(self, encoded_card):
        super().__init__()
        pic_name = _get_card_image_name(encoded_card)
        self.image = pygame.image.load(pic_name).convert()
        self.rect = self.image.get_rect()


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
