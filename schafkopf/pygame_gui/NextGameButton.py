import pygame
from typing import Tuple, Callable
from schafkopf.pygame_gui.Button import Button
from schafkopf.pygame_gui.colors import BLACK, WHITE


class NextGameButton(Button):
    def __init__(self, topleft: Tuple[int, int], callback: Callable, font_size: int = 40):
        margin = 10
        font = pygame.font.Font(None, font_size)
        text = font.render("Neues Spiel", True, BLACK)
        height = font_size + margin
        width = text.get_width() + 2 * margin
        image = pygame.Surface((width, height))
        image.fill(WHITE)
        image.set_alpha(180)
        image.blit(text, (margin, margin))
        button_down_image = pygame.Surface((width, height))
        button_down_image.fill(pygame.Color('grey'))
        button_down_image.set_alpha(180)
        button_down_image.blit(text, (margin, margin))
        hover_image = pygame.Surface((width + 5, height + 5))
        hover_image.fill(pygame.Color("lightgrey"))
        hover_image.set_alpha(180)
        hover_image.blit(text, (margin + 2, margin + 2))
        super().__init__(
            topleft=topleft,
            image=image,
            button_down_image=button_down_image,
            hover_image=hover_image,
            callback=callback
        )

