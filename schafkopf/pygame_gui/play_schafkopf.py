import random

import pygame
import sys

from schafkopf.card_deck import CardDeck
from schafkopf.pygame_gui.card import Card
from schafkopf.pygame_gui.game_state import new_game_state

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = width, height = screen.get_size()

background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)
all_sprites = pygame.sprite.Group()

card_deck = CardDeck()
leading_player_index = random.choice(range(4))

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    leading_player_index = 0

    screen.blit(background, (0, 0))

    game_state = new_game_state(card_deck, leading_player_index)
    player_hand_sprites = [Card(encoded_card) for encoded_card in game_state["player_hands"][0]]

    all_sprites.add(player_hand_sprites)
    for i, card_sprite in enumerate(player_hand_sprites):
        card_sprite.rect.bottomleft = (400 + i * 200, height - 200)

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

sys.exit()
