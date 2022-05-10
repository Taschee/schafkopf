import random

import pygame
import sys

from schafkopf.card_deck import CardDeck
from schafkopf.pygame_gui.card import OpenCard
from schafkopf.pygame_gui.card import HiddenCard
from schafkopf.pygame_gui.game_state import new_game_state

pygame.init()
pygame.display.set_caption("Schafkopf AI")

screen = pygame.display.set_mode((1440, 1020))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = width, height = screen.get_size()

num_cards = 8

space_between = 15
card_size = card_width, card_height = HiddenCard().rect.size
space_for_player_hand = num_cards * card_width + (num_cards - 1) * space_between

player_hand_position_height = height * 95 / 100
opposing_hand_position_height = height * 5 / 100 + card_height

player_hand_position_left = (width - space_for_player_hand) / 2
neighboring_hand_position_height = (height - space_for_player_hand) / 2
neighboring_hand_edge_distance = width * 5 / 100

background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)
all_sprites = pygame.sprite.Group()

card_deck = CardDeck()
leading_player_index = random.choice(range(4))
game_state = new_game_state(card_deck, leading_player_index)

player_hand_sprites = [OpenCard(encoded_card) for encoded_card in game_state["player_hands"][0]]
all_sprites.add(player_hand_sprites)

opponent_hand_sizes = [len(h) for h in game_state["player_hands"][1: 4]]

first_opponent_hand_sprites = [HiddenCard(rotate=True) for _ in range(opponent_hand_sizes[0])]
all_sprites.add(first_opponent_hand_sprites)

second_opponent_hand_sprites = [HiddenCard() for _ in range(opponent_hand_sizes[1])]
all_sprites.add(second_opponent_hand_sprites)

third_opponent_hand_sprites = [HiddenCard(rotate=True) for _ in range(opponent_hand_sizes[2])]
all_sprites.add(third_opponent_hand_sprites)


def main():
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
                print(clicked_sprites[0])

        for i, card_sprite in enumerate(player_hand_sprites):
            card_sprite.rect.bottomleft = (player_hand_position_left + i * (card_width + space_between),
                                           player_hand_position_height)

        for i, card_sprite in enumerate(first_opponent_hand_sprites):
            card_sprite.rect.bottomleft = (neighboring_hand_edge_distance,
                                           neighboring_hand_position_height + i * (card_width + space_between))

        for i, card_sprite in enumerate(second_opponent_hand_sprites):
            card_sprite.rect.bottomleft = (player_hand_position_left + i * (card_width + space_between),
                                           opposing_hand_position_height)

        for i, card_sprite in enumerate(third_opponent_hand_sprites):
            card_sprite.rect.bottomleft = (width - neighboring_hand_edge_distance - card_height,
                                           neighboring_hand_position_height + i * (card_width + space_between))

        screen.blit(background, (0, 0))

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
    sys.exit()
