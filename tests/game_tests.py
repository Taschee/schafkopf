#!/usr/bin/env python

from schafkopf.game import Game
from schafkopf.players import RandomPlayer

Alfons = RandomPlayer(name="Alfons")
Bertl = RandomPlayer(name="Bertha")
Chrissie = RandomPlayer(name="Chris")
Dora = RandomPlayer(name="Dora")

playerlist = [Alfons, Bertl, Chrissie, Dora]

cards = [(1, 1), (4, 0), (4, 1), (4, 2), (4, 3), (2, 0), (3, 2), (3, 3),
         (1, 0), (0, 0), (3, 1), (0, 1), (0, 2), (2, 2), (2, 3), (0, 3),
         (6, 0), (7, 1), (7, 0), (3, 0), (2, 1), (6, 2), (5, 0), (5, 1),
         (6, 1), (6, 3), (7, 2), (7, 3), (5, 2), (5, 3), (1, 2), (1, 3)]
testgame = Game(players=playerlist, leading_player_index=0, cards=cards, shuffle_cards=False)

testgame.decide_game_mode()
# testgame.define_trumpcards()
print("offensive players : ", testgame._offensive_players)
print("game mode :    ", testgame.get_game_mode())
print("trumpcards :  ", testgame._trump_cards)

while not testgame.finished():
    testgame.play_next_card()
    print("current player :    ", testgame.get_current_playerindex())
    print("current trick  :    ", testgame.get_current_trick().cards)
    print("Tricks :     ", testgame.get_tricks())
    testgame.trick_finished()

print("Final Scores : ", testgame._scores)
print("Winners : ", testgame.determine_winners())
print("Payout 0: ", testgame.get_payout(player=0))
print("Payout 1: ", testgame.get_payout(player=1))
print("Payout 2: ", testgame.get_payout(player=2))
print("Payout 3: ", testgame.get_payout(player=3))
print(testgame.num_laufende())
print(testgame.get_players()[0].get_starting_hand())
print(testgame.get_trump_cards()[0])
print(testgame.player_with_highest_trump())
