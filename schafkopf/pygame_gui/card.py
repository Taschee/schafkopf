import pygame

from schafkopf.ranks import *
from schafkopf.suits import *


class OpenCard(pygame.sprite.Sprite):
    def __init__(self, card_encoded):
        super().__init__()
        pic_name = self._get_card_image_name(card_encoded)
        self.image = pygame.image.load(pic_name).convert()
        self.rect = self.image.get_rect()
        self.card_encoded = card_encoded


    @staticmethod
    def _get_card_image_name(encoded_card):
        return "../images/" + rank_dict[encoded_card[0]] + suit_dict[encoded_card[1]] + ".jpg"


class HiddenCard(pygame.sprite.Sprite):
    def __init__(self, rotate: bool = False):
        super().__init__()
        pic_name = "../images/Rueckseite.jpg"
        if rotate:
            self.image = pygame.transform.rotate(pygame.image.load(pic_name).convert(), 90)
        else:
            self.image = pygame.image.load(pic_name).convert()
        self.rect = self.image.get_rect()


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
