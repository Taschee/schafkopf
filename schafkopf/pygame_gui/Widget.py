from typing import Tuple

import pygame


class Widget:
    def __init__(
        self,
        topleft: Tuple[int, int],
        image: pygame.Surface
    ):
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)
