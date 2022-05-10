import random

import pygame
import sys

from schafkopf.card_deck import CardDeck
from schafkopf.pygame_gui.card import OpenCard
from schafkopf.pygame_gui.card import HiddenCard
from schafkopf.pygame_gui.game_state import new_game_state

pygame.init()

# screen = pygame.display.set_mode((1440, 1080))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = width, height = screen.get_size()

background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)
all_sprites = pygame.sprite.Group()

card_deck = CardDeck()
leading_player_index = random.choice(range(4))
game_state = new_game_state(card_deck, leading_player_index)

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]

    player_hand_sprites = [OpenCard(encoded_card) for encoded_card in game_state["player_hands"][0]]
    all_sprites.add(player_hand_sprites)
    for i, card_sprite in enumerate(player_hand_sprites):
        card_sprite.rect.bottomleft = (40 + i * 100, height - 20)

    opponent_hand_sizes = [len(h) for h in game_state["player_hands"][1: 4]]

    first_opponent_hand_sprites = [HiddenCard(rotate=True) for _ in range(opponent_hand_sizes[0])]
    all_sprites.add(first_opponent_hand_sprites)
    for i, card_sprite in enumerate(first_opponent_hand_sprites):
        card_sprite.rect.bottomleft = (20, 40 + i * 100)

    second_opponent_hand_sprites = [HiddenCard() for _ in range(opponent_hand_sizes[1])]
    all_sprites.add(second_opponent_hand_sprites)
    for i, card_sprite in enumerate(second_opponent_hand_sprites):
        card_sprite.rect.bottomleft = (40 + i * 100, 200)

    third_opponent_hand_sprites = [HiddenCard(rotate=True) for _ in range(opponent_hand_sizes[2])]
    all_sprites.add(third_opponent_hand_sprites)
    for i, card_sprite in enumerate(third_opponent_hand_sprites):
        card_sprite.rect.bottomleft = (1000, 40 + i * 100)

    screen.blit(background, (0, 0))

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

sys.exit()
