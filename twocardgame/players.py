
import random


class Player:
    def __init__(self, name="Rando Calrissian"):
        self._name = name
        self._hand = []
        return

    def pick_up_cards(self, hand):
        self._hand = hand
        self.sort_hand()

    def number_of_cards(self):
        return len(self._hand)

    def get_hand(self):
        return self._hand

    def sort_hand(self):
        trumps_in_hand = [trump for trump in [(3,0), (2,0), (1,0)] if trump in self._hand]
        schellen = [(i, 1) for i in range(3, -1, -1) if (i, 1) in self._hand]
        sorted_hand = trumps_in_hand + schellen
        self._hand = sorted_hand

class RandomPlayer(Player):

    def choose_game_mode(self, options):
        return random.choice(tuple(options))

    def play_card(self, previous_cards, options=None, card=None):
        if options is None:
            card = random.choice(self._hand)
        else:
            card = random.choice(options)
        self._hand.remove(card)
        return card

class CFRPlayer(Player):

    def choose_game_mode(self, options):
        return 0

    def play_card(self, previous_cards, options=None, card=None):
        if card is not None:
            if card not in options:
                print("Card not legal")
            else:
                self._hand.remove(card)
                return card
        if card is None:
            if options is None:
                return random.choice(self._hand)
            else:
                return random.choice(options)


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
