import random
from twocardgame.twocardgame import TwoCardGame

WEITER = 0
SOLO = 1

class Node:
    def __init__(self, infoset):
        self.infoset = infoset
        if "game_mode" not in infoset.keys():
            self.number_of_actions = 2
        else:
            self.number_of_actions = len(infoset["possible_cards"])
        self.cumulative_regrets = [0 for n in range(self.number_of_actions)]
        self.cumulative_strategies = [0 for n in range(self.number_of_actions)]

    def get_strategy(self, weight=1):
        norm_sum = sum(self.cumulative_regrets)
        if norm_sum == 0:
            strategy = [1/self.number_of_actions for i in range(self.number_of_actions)]
        else:
            strategy = [1 / norm_sum * regret for regret in self.cumulative_regrets]
        self.cumulative_strategies = [self.cumulative_strategies[i] + weight*strategy[i]
                                      for i in range(self.number_of_actions)]
        return strategy

    def get_average_strategy(self):
        norm_sum = sum(self.cumulative_strategies)
        if norm_sum == 0:
            av_strategy = [1 / self.number_of_actions for i in range(self.number_of_actions)]
        else:
            av_strategy = [1 / norm_sum * strat for strat in self.cumulative_strategies]
        return av_strategy

class NodeMap:
    def __init__(self):
        self._nodes = []
        self._infosets = []

    def add_node(self, node):
        self._nodes.append(node)
        self._infosets.append(node.infoset)

    def get_node(self, infoset):
        if infoset in self._infosets:
            index = self._infosets.index(infoset)
            return self._nodes[index]

class CFRTrainer:
    def __init__(self, agent):
        self.node_map = NodeMap()
        self.player = agent

    def cfr(self):
        return

    def train(self, iterations):
        for i in range(iterations):
            game = TwoCardGame([self.player, self.player, self.player])
