from twocardgame.twocardgame import TwoCardGame
from twocardgame.cfr_again import CFRTrainer, NodeMap, Node, History
from twocardgame.players import RandomPlayer, CFRPlayer

cards = [(3, 0), (2, 1), (2, 0), (1, 0), (3, 1), (1, 1)]
cards_played = []
history = History(mode_proposals=[], cards_played=cards_played, starting_deck=cards)

history += 1
history += 0
history += 0

history += (3, 0)
history += (1, 0)
history += (1, 1)

print(history.get_offensive_player())
print(history.is_terminal())
print(history.calculate_score(1))
print(history.get_payout(1))

