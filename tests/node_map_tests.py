from twocardgame.cfr import NodeMap, History

node_map = NodeMap()

cards = [(1, 1), (2, 1), (3, 0), (2, 0), (3, 1), (1, 0)]
cards_played = []
history = History(mode_proposals=[], cards_played=cards_played, starting_deck=cards)

current_player = history.get_current_player()

private_cards = cards[2 * current_player: 2 * current_player + 2 ]
infoset = (private_cards, history.mode_proposals, history.cards_played)
node = node_map.get_node(infoset)


print(node_map.get_infosets())
print(node.cumulative_regrets)
print(node.get_strategy())

node.cumulative_regrets[0] += 1

node = node_map.get_node(infoset=infoset)
print(node_map.get_infosets())
print(node.cumulative_regrets)
print(node.get_strategy())

node.cumulative_regrets[1] += 2

node = node_map.get_node(infoset=infoset)
print(node_map.get_infosets())
print(node.cumulative_regrets)
print(node.get_strategy())

action = 0
new_history = history + action

current_player = new_history.get_current_player()

private_cards = cards[2 * current_player: 2 * current_player + 2 ]
infoset = (private_cards, new_history.mode_proposals, new_history.cards_played)
node = node_map.get_node(infoset)

print(node_map.get_infosets())
print(node.cumulative_regrets)
print(node.get_strategy())

