#!/usr/bin/env python3

import os
import pygame
from schafkopf.game import Game
from schafkopf.players import RandomPlayer

pygame.init()

SUITS = {"0": "Schellen", "1": "Herz", "2": "Gras", "3": "Eichel"}
SYMBOLS = {"0": "7", "1": "8", "2": "9", "3": "U", "4": "O", "5": "K", "6": "10", "7": "A"}


class Card(pygame.sprite.Sprite):
    def __init__(self, card, face_down=False, angle=0, size=None):
        pygame.sprite.Sprite.__init__(self)
        self.card = card
        self.angle = angle
        self.size = size
        self.face_down = face_down
        file = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
        self.frontside = self.transform(pygame.image.load(os.path.join("images", file)).convert())
        self.backside = self.transform(pygame.image.load(os.path.join("images", "Rueckseite.jpg")).convert())
        if face_down:
            self.image = self.backside
        else:
            self.image = self.frontside
        self.rect = self.image.get_rect()
        self.in_current_trick = False

    def transform(self, image):
        if self.size is not None:
            image = pygame.transform.scale(image, self.size)
        return pygame.transform.rotate(image, self.angle)

    def turn_over(self):
        if self.face_down:
            self.image = self.frontside
            self.face_down = False
        else:
            self.image = self.backside
            self.face_down = True

class TableViewer:
    def __init__(self, screensize, playerlist, current_game):
        self.screensize = screensize
        self.current_game = current_game
        self.cardsize = screensize[0] * 7 // 100, screensize[1] * 14 // 100
        self.playerlist = playerlist

    def prepare_hand(self, player, angle):
        hand = [Card(card, angle=angle, size=self.cardsize) for card in player.get_hand()]
        if self.playerlist.index(player) == 0:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] / 5 + i * self.screensize[0] * 75 / 1000,
                                     self.screensize[1] * (83 / 100))
        elif self.playerlist.index(player) == 1:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] * 83 / 100,
                                     self.screensize[0] / 5 + i * self.screensize[1] * 75 / 1000)
        elif self.playerlist.index(player) == 2:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] / 5 + i * self.screensize[0] * 75 / 1000,
                                     self.screensize[1] * 3 / 100)
        elif self.playerlist.index(player) == 3:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] * 3 / 100,
                                     self.screensize[0] / 5 + i * self.screensize[1] * 75 / 1000)
        return hand

    def prepare_current_trick(self):
        pos_curr_trick = [(self.screensize[0] * 465 // 1000, self.screensize[1] * 55 // 100),
                          (self.screensize[0] * 55 // 100, self.screensize[1] * 465 // 1000),
                          (self.screensize[0] * 465 // 1000, self.screensize[1] * 31 // 100),
                          (self.screensize[0] * 31 // 100, self.screensize[1] * 465 // 1000)]
        curr_trick = self.current_game.get_current_trick()
        curr_trick_sprites = []
        for card, i in zip(curr_trick.cards, range(4)):
            if card is not None:
                sprite = Card(card, angle=90*i, size=self.cardsize)
                sprite.rect.topleft = pos_curr_trick[i]
                curr_trick_sprites.append(sprite)
        return curr_trick_sprites

def main():
    screensize = (700, 700)
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption('Schafkopf!')
    brown = [139, 69, 19]
    screen.fill(brown)
    pygame.display.flip()


    Alfons = RandomPlayer(name="Alfons")
    Bertl = RandomPlayer(name="Bertha")
    Chrissie = RandomPlayer(name="Chris")
    Dora = RandomPlayer(name="Dora")
    playerlist = [Alfons, Bertl, Chrissie, Dora]

    game = Game(players=playerlist, leading_player_index=0)

    game.decide_game_mode()

    for player in game.get_players():
        player.sort_hand(trumpcards=game.get_trump_cards())

    viewer = TableViewer(screensize=(600,600), playerlist=playerlist, current_game=game)

    screen.fill(brown)
    all_cards = viewer.prepare_current_trick()
    for player, i in zip(playerlist, range(len(playerlist))):
        hand = viewer.prepare_hand(player=player, angle=i * 90)
        all_cards.append(hand)

    all_sprites = pygame.sprite.RenderPlain(all_cards)

    all_sprites.draw(screen)
    pygame.display.flip()

    running = True
    while running:
        for ev in pygame.event.get():


            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONUP:

                if not game.finished():
                    game.play_next_card()

                    screen.fill(brown)

                    all_cards = viewer.prepare_current_trick()

                    for player, i in zip(playerlist, range(len(playerlist))):
                        hand = viewer.prepare_hand(player=player, angle=i * 90)
                        all_cards.append(hand)

                    all_sprites = pygame.sprite.RenderPlain(all_cards)

                    all_sprites.draw(screen)
                    pygame.display.flip()

                    game.trick_finished()

                else:
                    screen.fill(brown)
                    winner_indices = game.determine_winners()
                    winner_names = [playerlist[i]._name for i in winner_indices]



if __name__ == "__main__":
    main()
