import time

import pygame

from schafkopf.game_modes import NO_GAME
from schafkopf.pygame_gui.BiddingOption import BiddingOption
from schafkopf.pygame_gui.BiddingProposal import BiddingProposal
from schafkopf.pygame_gui.HiddenCard import HiddenCard
from schafkopf.pygame_gui.ResultWidget import ResultWidget
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame
from schafkopf.pygame_gui.OpenCard import OpenCard

pygame.init()
pygame.font.init()

pygame.display.set_caption("Schafkopf AI")

# screen = pygame.display.set_mode((1440, 1020))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
screen_size = screen_width, screen_height = screen.get_size()
background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)

space_between = 15
card_size = card_width, card_height = HiddenCard().rect.size

player_hand_position_height = screen_height * 95 / 100
opposing_hand_position_height = screen_height * 5 / 100 + card_height
neighboring_hand_edge_distance = screen_width * 5 / 100

bidding_option_position_left = int(screen_width * 40 / 100)
bidding_option_position_height = int(screen_height * 30 / 100)
bidding_font_size = int(screen_height * 4 / 100)
bidding_option_space_between = bidding_font_size + 15

current_trick_human_pos = (int(screen_width * 50 / 100), int(screen_height * 60 / 100))
current_trick_first_opp_pos = (int(screen_width * 40 / 100), int(screen_height * 50 / 100))
current_trick_second_opp_pos = (int(screen_width * 50 / 100), int(screen_height * 40 / 100))
current_trick_third_opp_pos = (int(screen_width * 60 / 100), int(screen_height * 50 / 100))
current_trick_positions = [
    current_trick_human_pos, current_trick_first_opp_pos, current_trick_second_opp_pos, current_trick_third_opp_pos
]

game_mode_position_human = (int(screen_width * 45 / 100), int(screen_height * 80 / 100))
game_mode_position_first_opp = (int(screen_width * 15 / 100), int(screen_height * 50 / 100))
game_mode_position_second_opp = (int(screen_width * 45 / 100), int(screen_height * 20 / 100))
game_mode_position_third_opp = (int(screen_width * 78 / 100), int(screen_height * 50 / 100))
game_mode_positions = [
    game_mode_position_human, game_mode_position_first_opp, game_mode_position_second_opp, game_mode_position_third_opp
]

result_widget_position = (screen_width // 4, screen_height // 4)

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bidding_sprites = pygame.sprite.Group()
current_trick_sprites = pygame.sprite.Group()


def space_for_player_hand(num_cards):
    return num_cards * card_width + (num_cards - 1) * space_between


def player_hand_position_left(num_cards):
    return (screen_width - space_for_player_hand(num_cards)) / 2


def neighboring_hand_position_height(num_cards):
    return (screen_height - space_for_player_hand(num_cards)) / 2


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
            screen_width - neighboring_hand_edge_distance - card_height,
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
    bidding_options = [BiddingOption((200, 200), o, screen_height // 25) for o in options]
    bidding_sprites.add(bidding_options)
    all_sprites.add(bidding_options)
    for i, bid_sprite in enumerate(bidding_sprites):
        bid_sprite.rect.bottomleft = (bidding_option_position_left,
                                      bidding_option_position_height + i * bidding_option_space_between)


def display_last_opponent_bids(schafkopf_game):
    leading_player_index = schafkopf_game.game_state["leading_player_index"]
    proposals = schafkopf_game.game_state["mode_proposals"]
    for i, proposal in enumerate(proposals):
        if proposal is not None:
            screen.blit(
                BiddingProposal(
                    proposal[0] == NO_GAME,
                    screen_width // 10,
                    screen_height // 20
                ),
                game_mode_positions[(leading_player_index + i) % 4]
            )


def display_current_trick(schafkopf_game):
    current_trick = schafkopf_game.game_state["current_trick"].cards
    for i, card_encoded in enumerate(current_trick):
        if card_encoded is not None:
            current_trick_sprites.add(OpenCard(card_encoded, current_trick_positions[i]))
    all_sprites.add(current_trick_sprites)


def display_game_mode(schafkopf_game):
    pos = game_mode_positions[schafkopf_game.game_state["declaring_player"]]
    game_mode = BiddingOption(pos, schafkopf_game.game_state["game_mode"], screen_height // 25)
    all_sprites.add(game_mode)


def display_results(schafkopf_game):
    screen.blit(
        ResultWidget(schafkopf_game, screen_width // 2, screen_height // 2),
        result_widget_position
    )


def next_human_bid(schafkopf_game, event_list):
    if schafkopf_game.human_players_turn():
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                for bid_sprite in bidding_sprites:
                    if bid_sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        print(bid_sprite.option)
                        schafkopf_game.next_human_bid(bid_sprite.option)
                        print(schafkopf_game.game_state)


def next_human_card(schafkopf_game, event_list):
    if schafkopf_game.human_players_turn():
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                for card_sprite in player_sprites:
                    if card_sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        print(card_sprite.card_encoded)
                        schafkopf_game.next_human_card(card_sprite.card_encoded)
                        print(schafkopf_game.game_state)


def main():
    leading_player_index = 0
    schafkopf_game = SchafkopfGame(leading_player_index)

    done = False
    while not done:
        event_list = pygame.event.get()

        all_sprites.empty()
        player_sprites.empty()
        bidding_sprites.empty()
        current_trick_sprites.empty()

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

        if not schafkopf_game.bidding_is_finished():
            if schafkopf_game.human_players_turn():
                options = schafkopf_game.possible_bids()
                display_possible_player_bids(options)

                next_human_bid(schafkopf_game, event_list)
            else:
                time.sleep(1)
                schafkopf_game.next_action()

            display_last_opponent_bids(schafkopf_game)
        elif not schafkopf_game.finished():
            display_game_mode(schafkopf_game)
            display_current_trick(schafkopf_game)
            if schafkopf_game.human_players_turn():
                next_human_card(schafkopf_game, event_list)
            else:
                time.sleep(0.5)
                schafkopf_game.next_action()
        else:
            display_results(schafkopf_game)

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
