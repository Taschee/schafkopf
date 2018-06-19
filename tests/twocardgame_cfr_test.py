from twocardgame.cfr import Node, NodeMap, CFRTrainer, History
import random

node_map = NodeMap()

cards = [(1, 1), (2, 1), (3, 0), (2, 0), (3, 1), (1, 0)]
cards_played = []
history = History(mode_proposals=[], cards_played=cards_played, starting_deck=cards)

current_player = history.get_current_player()

private_cards = cards[2 * current_player: 2 * current_player + 2 ]
infoset = (private_cards, history.mode_proposals, history.cards_played)
node = node_map.get_node(infoset)


strategy = node.get_strategy()

node_util = 0

util = [0 for i in range(node.number_of_actions)]

action = node.actions[0]
new_history = history + action

cfr_trainer = CFRTrainer()

cfr_trainer.train(1, shuffle=False)
