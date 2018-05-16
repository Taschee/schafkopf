#!/usr/bin/env python3

import pygame
from schafkopf.players import RandomPlayer
from schafkopf.game import Game

pygame.init()

suit_dict = {"0": "Schellen", "1": "Herz", "2": "Gras", "3": "Eichel"}
symbol_dict = {"0": "7", "1": "8", "2": "9", "3": "U", "4": "O", "5": "K", "6": "10", "7": "A"}


def load_card_image(card):
    next_card = symbol_dict[str(card[0])] + suit_dict[str(card[1])]
    card_surf = pygame.image.load('../images/' + next_card + '.jpg').convert()
    return card_surf


def display_card(card, loc, screen, screensize, angle=0,):
    width = screensize[0] * 7 // 100
    height = screensize[1] * 14 // 100
    card_surf = pygame.transform.scale(load_card_image(card), (width, height))
    rotated_surf = pygame.transform.rotate(card_surf, angle)
    screen.blit(rotated_surf, loc)


def display_hand(player, locs, screen, screensize, angle=0):
    hand = player.get_hand()
    for card, loc in zip(hand, locs):
        display_card(card, loc, screen, screensize, angle)


def display_all_hands(game, all_hand_locs, screen, screensize):
    angle = 0
    players = game.get_players()
    for player, loc in zip(players, all_hand_locs):
        display_hand(player, loc, screen, screensize, angle)
        angle += 90


def display_current_trick(game, loc_played_cards, screen, screensize):
    current_trick = game.get_current_trick()
    for card in current_trick.cards:
        if card is not None:
            player_index = current_trick.cards.index(card)
            angle = player_index * 90
            loc = loc_played_cards[player_index]
            display_card(card, loc, screen, screensize, angle)


def update_table(game, all_hand_locs, locs_played_cards, screen, screensize):
    display_all_hands(game, all_hand_locs, screen, screensize)
    display_current_trick(game, locs_played_cards, screen, screensize)
    pygame.display.update()


def main():
    SCREENSIZE = (700, 700)

    loc_player0 = [(SCREENSIZE[0] / 5 + i * SCREENSIZE[0] * 75 / 1000, SCREENSIZE[1] * (83 / 100)) for i in range(8)]
    loc_player1 = [(SCREENSIZE[0] * 83 / 100, SCREENSIZE[0] / 5 + i * SCREENSIZE[1] * 75 / 1000) for i in range(8)]
    loc_player2 = [(SCREENSIZE[0] / 5 + i * SCREENSIZE[0] * 75 / 1000, SCREENSIZE[1] * 3 / 100) for i in range(8)]
    loc_player3 = [(SCREENSIZE[0] * 3 / 100, SCREENSIZE[0] / 5 + i * SCREENSIZE[1] * 75 / 1000) for i in range(8)]
    all_hand_locs = [loc_player0, loc_player1, loc_player2, loc_player3]

    loc_played_cards = [(SCREENSIZE[0] * 465 // 1000, SCREENSIZE[1] * 55 // 100),
                        (SCREENSIZE[0] * 55 // 100, SCREENSIZE[1] * 465 // 1000),
                        (SCREENSIZE[0] * 465 // 1000, SCREENSIZE[1] * 31 // 100),
                        (SCREENSIZE[0] * 31 // 100, SCREENSIZE[1] * 465 // 1000)]

    Alfons = RandomPlayer(name="Alfons")
    Bertl = RandomPlayer(name="Bertha")
    Chrissie = RandomPlayer(name="Chris")
    Dora = RandomPlayer(name="Dora")
    playerlist = [Alfons, Bertl, Chrissie, Dora]

    game = Game(players=playerlist, leading_player_index=0)

    game.decide_game_mode()

    for player in game.get_players():
        player.sort_hand(trumpcards=game._trump_cards)

    game.play_next_card()
    game.trick_finished()
    game.play_next_card()

    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Schafkopf!')

    brown = [139, 69, 19]
    screen.fill(brown)
    pygame.display.flip()

    running = True
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()
            else:
                update_table(game, all_hand_locs, loc_played_cards, screen, screensize=SCREENSIZE)


if __name__ == "__main__":
    main()
