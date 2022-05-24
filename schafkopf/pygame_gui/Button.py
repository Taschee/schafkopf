from typing import Tuple, Callable

import pygame


class Button:
    def __init__(
        self,
        topleft: Tuple[int, int],
        image: pygame.Surface,
        button_down_image: pygame.Surface = None,
        hover_image: pygame.Surface = None,
        callback: Callable = None
    ):
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        self.pressed = False
        self.callback = callback
        self.button_up_image = image
        if button_down_image is not None:
            self.button_down_image = button_down_image
        else:
            self.button_down_image = image
        if hover_image is not None:
            self.hover_image = hover_image
        else:
            self.hover_image = image

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.button_down_image
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.image = self.image
            if self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback is not None:
                    self.callback()
        elif not self.pressed:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
            else:
                self.image = self.button_up_image
