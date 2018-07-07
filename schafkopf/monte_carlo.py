from copy import deepcopy
from schafkopf.game import Game
from schafkopf.players import Player
from schafkopf.helpers import sample_opponent_cards
import numpy as np


UCB_CONSTANT = 2


class MCNode:
    def __init__(self, state, current_player, parent=None, previous_action=None):
        self.children = []
        self.parent = parent
        self.state = state
        self.current_player = current_player
        self.previous_action = previous_action
        self.visits = 0
        self.cumulative_rewards = [0 for i in range(4)]

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def best_child(self):
        if not self.is_leaf():
            values = [self.ucb_value(child) for child in self.children]
            best_child = self.children[np.argmax(values)]
            return best_child

    def ucb_value(self, child_node):
        if child_node.visits != 0:
            average_reward = self.get_average_reward(player=self.current_player)
            return average_reward + UCB_CONSTANT * np.sqrt(2 * np.log(self.visits) / child_node.visits)
        else:
            return np.infty

    def update_visits(self):
        self.visits += 1

    def update_rewards(self, rewards):
        for i in range(len(self.cumulative_rewards)):
            self.cumulative_rewards[i] += rewards[i]

    def get_average_reward(self, player):
        if self.visits > 0:
            return self.cumulative_rewards[player] / self.visits
        else:
            return 0

class MCTree:
    def __init__(self, root_node):
        self.root_node = root_node
        self.nodes = {root_node}

    def add_node(self, node, parent_node):
        self.nodes.add(node)
        parent_node.add_child(node)

    def backpropagate(self, leaf_node, rewards):
        current_node = leaf_node
        while current_node != self.root_node:
            current_node.update_rewards(rewards)
            current_node.update_visits()
            current_node = current_node.parent
