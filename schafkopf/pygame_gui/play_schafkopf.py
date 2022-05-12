import sys
import pygame

from schafkopf.pygame_gui.BiddingOption import BiddingOption
from schafkopf.pygame_gui.HiddenCard import HiddenCard
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame
from schafkopf.pygame_gui.OpenCard import OpenCard

pygame.init()
pygame.font.init()

pygame.display.set_caption("Schafkopf AI")

screen = pygame.display.set_mode((1440, 1020))
screen_size = width, height = screen.get_size()
background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)

space_between = 15
card_size = card_width, card_height = HiddenCard().rect.size

player_hand_position_height = height * 95 / 100
opposing_hand_position_height = height * 5 / 100 + card_height
neighboring_hand_edge_distance = width * 5 / 100

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bidding_sprites = pygame.sprite.Group()
trick_sprites = pygame.sprite.Group()


def space_for_player_hand(num_cards):
    return num_cards * card_width + (num_cards - 1) * space_between


def player_hand_position_left(num_cards):
    return (width - space_for_player_hand(num_cards)) / 2


def neighboring_hand_position_height(num_cards):
    return (height - space_for_player_hand(num_cards)) / 2


def next_move(schafkopf_game, event_list):
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_player_cards = [s for s in player_sprites if s.rect.collidepoint(pygame.mouse.get_pos())]
            if len(clicked_player_cards) > 0:
                print(clicked_player_cards[0].card_encoded)


def display_opponent_hands(schafkopf_game):
    opponent_hand_sizes = [len(h) for h in schafkopf_game.game_state["player_hands"][1: 4]]
    first_opponent_hand_sprites = [HiddenCard(rotate=True) for _ in range(opponent_hand_sizes[0])]
    all_sprites.add(first_opponent_hand_sprites)
    second_opponent_hand_sprites = [HiddenCard() for _ in range(opponent_hand_sizes[1])]
    all_sprites.add(second_opponent_hand_sprites)
    third_opponent_hand_sprites = [HiddenCard(rotate=True) for _ in range(opponent_hand_sizes[2])]
    all_sprites.add(third_opponent_hand_sprites)
    for i, card_sprite in enumerate(first_opponent_hand_sprites):
        card_sprite.rect.bottomleft = (
            neighboring_hand_edge_distance,
            neighboring_hand_position_height(len(first_opponent_hand_sprites)) + i * (card_width + space_between)
        )
    for i, card_sprite in enumerate(second_opponent_hand_sprites):
        card_sprite.rect.bottomleft = (
            player_hand_position_left(len(second_opponent_hand_sprites)) + i * (card_width + space_between),
            opposing_hand_position_height
        )
    for i, card_sprite in enumerate(third_opponent_hand_sprites):
        card_sprite.rect.bottomleft = (
            width - neighboring_hand_edge_distance - card_height,
            neighboring_hand_position_height(len(third_opponent_hand_sprites)) + i * (card_width + space_between)
        )


def display_player_hand(schafkopf_game):
    player_hand_sprites = [OpenCard(encoded_card) for encoded_card in schafkopf_game.game_state["player_hands"][0]]
    all_sprites.add(player_hand_sprites)
    player_sprites.add(player_hand_sprites)
    for i, card_sprite in enumerate(player_hand_sprites):
        card_sprite.rect.bottomleft = (
            player_hand_position_left(len(player_hand_sprites)) + i * (card_width + space_between),
            player_hand_position_height
        )


def display_possible_player_bids(options):
    bidding_options = [BiddingOption((200, 200), o) for o in options]
    bidding_sprites.add(bidding_options)
    all_sprites.add(bidding_options)
    for i, card_sprite in enumerate(bidding_sprites):
        card_sprite.rect.bottomleft = (
            400,
            300 + i * 50
        )


def display_current_trick(trick):
    pass


def main():
    leading_player_index = 0
    schafkopf_game = SchafkopfGame(leading_player_index)

    done = False
    while not done:
        event_list = pygame.event.get()

        all_sprites.empty()
        player_sprites.empty()
        bidding_sprites.empty()

        for event in event_list:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_n:
                    leading_player_index = (leading_player_index + 1) % 4
                    schafkopf_game = SchafkopfGame(leading_player_index)

        screen.blit(background, (0, 0))

        display_player_hand(schafkopf_game)
        display_opponent_hands(schafkopf_game)

        options = schafkopf_game.possible_actions()
        if not schafkopf_game.bidding_is_finished():
            display_possible_player_bids(options)
        elif not schafkopf_game.finished():
            display_current_trick(schafkopf_game.game_state["current_trick"])

        all_sprites.draw(screen)

        next_move(schafkopf_game, event_list)

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
