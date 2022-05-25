from typing import Tuple

import pygame

from schafkopf.pygame_gui.Widget import Widget


class OpponentCard(Widget):
    def __init__(
        self,
        topleft: Tuple[int, int] = (0, 0),
        rotate: bool = False
    ):
        pic_name = "../images/Rueckseite.jpg"
        if rotate:
            self.image = pygame.transform.rotate(pygame.image.load(pic_name).convert(), 90)
        else:
            self.image = pygame.image.load(pic_name).convert()
        super().__init__(topleft, self.image)
