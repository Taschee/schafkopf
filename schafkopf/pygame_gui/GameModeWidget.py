from typing import Union, Tuple, Callable

import pygame

from schafkopf.game_modes import *
from schafkopf.pygame_gui.Button import Button
from schafkopf.pygame_gui.colors import WHITE, BLACK, RED


class GameModeWidget(Button):
    def __init__(
        self,
        topleft: Tuple[int, int] = (0, 0),
        bidding_option: Tuple[int, Union[int, None]] = (NO_GAME, None),
        callback: Callable = None,
        font_size: int = 40,
        clickable: bool = True
    ):
        margin = 10
        font = pygame.font.Font(None, font_size)
        text = font.render(get_bidding_option_as_text(bidding_option), True, BLACK)
        height = font_size
        width = text.get_width() + 2 * margin
        image = pygame.Surface((width, height))
        image.fill(WHITE)
        image.set_alpha(180)
        image.blit(text, (margin, margin))
        if clickable:
            button_down_image = pygame.Surface((width, height))
            button_down_image.fill(pygame.Color('grey'))
            button_down_image.set_alpha(180)
            button_down_image.blit(text, (margin, margin))
            hover_image = pygame.Surface((width + 5, height + 5))
            hover_image.fill(pygame.Color("lightgrey"))
            hover_image.set_alpha(180)
            hover_image.blit(text, (margin + 2, margin + 2))
        else:
            button_down_image = image
            hover_image = image
        super().__init__(
            topleft=topleft,
            image=image,
            button_down_image=button_down_image,
            hover_image=hover_image,
            callback=callback
        )


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
