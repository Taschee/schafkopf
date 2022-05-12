import pygame


class HiddenCard(pygame.sprite.Sprite):
    def __init__(self, rotate: bool = False):
        super().__init__()
        pic_name = "../images/Rueckseite.jpg"
        if rotate:
            self.image = pygame.transform.rotate(pygame.image.load(pic_name).convert(), 90)
        else:
            self.image = pygame.image.load(pic_name).convert()
        self.rect = self.image.get_rect()
