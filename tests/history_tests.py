from twocardgame.twocardgame import TwoCardGame
from twocardgame.cfr import CFRTrainer, NodeMap, Node, History
from twocardgame.players import RandomPlayer, CFRPlayer

cards = [(1, 0), (2, 1), (2, 0), (3, 0), (1, 1), (3, 1)]
cards_played = []
history = History(mode_proposals=[], cards_played=cards_played, starting_deck=cards)

history += 0
history += 1
history += 0

history += (1, 0)
history += (2, 0)
history += (3, 1)

print(history.get_offensive_player())
print(history.is_terminal())
print(history.calculate_score(2))
print(history.get_payout(2))

player = 0
node_map = NodeMap()
private_cards = cards[2 * player: 2 * player + 2 ]
infoset = (private_cards, history.mode_proposals, history.cards_played)
node = node_map.get_node(infoset)

print(node.actions)
print(node.cumulative_regrets)

