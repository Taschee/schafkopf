import random


WEITER = 0
SOLO = 1
TRUMPCARDS = [(3,0), (2,0), (1,0)]

class Node:
    def __init__(self, infoset):
        self.infoset = infoset
        if len(infoset[1]) < 3:
            if SOLO in infoset[1]:
                self.actions = [WEITER]
            else:
                self.actions = [WEITER, SOLO]
        else:
            self.actions = self.possible_cards()
        self.number_of_actions = len(self.actions)
        self.cumulative_regrets = [0 for n in range(self.number_of_actions)]
        self.cumulative_strategies = [0 for n in range(self.number_of_actions)]
        self.current_strategy = None
        self.update_strategy()

    def possible_cards(self):
        if len(self.infoset[2]) == 0:
            return self.infoset[0]
        else:
            first_card = self.infoset[2][0]
            if first_card in TRUMPCARDS:
                players_trumpcards = [trump for trump in TRUMPCARDS if trump in self.infoset[0]]
                if len(players_trumpcards) > 0:
                    return players_trumpcards
                else:
                    return self.infoset[0]
            else:
                suit = first_card[1]
                return self.suit_in_hand(suit, hand=self.infoset[0])

    def suit_in_hand(self, suit, hand):
        suit_cards = [card for card in hand if card[1] == suit and card not in TRUMPCARDS]
        if len(suit_cards) > 0:
            return suit_cards
        else:
            return hand

    def update_strategy(self, weight=1):
        norm_sum = sum([regret for regret in self.cumulative_regrets if regret > 0])
        if norm_sum == 0:
            strategy = [1/self.number_of_actions for i in range(self.number_of_actions)]
        else:
            strategy = [max(1 / norm_sum * regret, 0) for regret in self.cumulative_regrets]
        for i in range(self.number_of_actions):
            self.cumulative_strategies[i] += weight * strategy[i]
        self.current_strategy = strategy
        return strategy

    def get_strategy(self):
        return self.current_strategy

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
            node = self._nodes[index]
        else:
            node = Node(infoset)
            self.add_node(node)
        return node

    def get_infosets(self):
        return self._infosets

    def get_nodes(self):
        return self._nodes


class History:
    def __init__(self, mode_proposals, cards_played, starting_deck):
        self.mode_proposals = mode_proposals
        self.cards_played = cards_played
        self.starting_deck = starting_deck

    def __add__(self, action):
        new_proposals = self.mode_proposals[:]
        new_cards_played = self.cards_played[:]
        if type(action) is int:
            new_proposals.append(action)
        elif type(action) is tuple:
            new_cards_played.append(action)
        else:
            raise TypeError("Action is neither integer (mode proposal) nor tuple (card)")
        return History(new_proposals, new_cards_played, self.starting_deck)

    def to_string(self):
        return str(self.mode_proposals) + str(self.cards_played)

    def game_mode_decided(self):
        if len(self.mode_proposals) == 3:
            return True
        else:
            return False

    def get_current_player(self):
        if not self.game_mode_decided():
            return len(self.mode_proposals)
        else:
            return len(self.cards_played) % 3

    def is_terminal(self):
        if len(self.mode_proposals) == 3 and sum(self.mode_proposals) == 0:
            return True
        elif len(self.cards_played) == 3:
            return True
        else:
            return False

    def get_offensive_player(self):
        for player in range(len(self.mode_proposals)):
            if self.mode_proposals[player] == 1:
                return player

    def determine_trickwinner(self, trick, leading_player):
        # cards in order how they were played
        winning_card = trick[0]
        winner = leading_player
        for card, i in zip(trick[1:], [1,2]):
            if winning_card not in TRUMPCARDS:
                if card in TRUMPCARDS or card[0] > winning_card[0] and card[1] == winning_card[1]:
                    winning_card = card
                    winner = (leading_player + i) % 3
            else:
                if card in TRUMPCARDS and card[0] > winning_card[0]:
                    winning_card = card
                    winner = (leading_player + i) % 3
        return winner

    def calculate_score(self, player):
        offensive_player = self.get_offensive_player()
        first_trick = self.cards_played[:3]
        winner_first_trick = self.determine_trickwinner(first_trick, leading_player=0)
        rest_of_deck = [card for card in self.starting_deck if card not in first_trick]
        second_trick = [rest_of_deck[winner_first_trick],
                        rest_of_deck[(winner_first_trick + 1) % 3],
                        rest_of_deck[(winner_first_trick + 2) % 3]]
        winner_second_trick = self.determine_trickwinner(second_trick, leading_player=winner_first_trick)
        score_offensive_player = 0
        if winner_first_trick == offensive_player:
            score_offensive_player += sum([card[0] for card in first_trick])
        if winner_second_trick == offensive_player:
            score_offensive_player += sum([card[0] for card in second_trick])
        if player == offensive_player:
            return score_offensive_player
        else:
            return 12 - score_offensive_player

    def get_payout(self, player):
        if sum(self.mode_proposals) == 0:
            return 0
        else:
            offensive_player = self.get_offensive_player()
            score_offensive_player = self.calculate_score(offensive_player)
            if player == offensive_player:
                if score_offensive_player > 6:
                    return 2
                else:
                    return -2
            else:
                if score_offensive_player > 6:
                    return -1
                else:
                    return 1


class CFRTrainer:
    def __init__(self):
        self.node_map = NodeMap()

    def adapt_payout(self, history, new_history):
        # not sure if useful
        player = history.get_current_player()
        next_player = new_history.get_current_player()
        if player == history.get_offensive_player():
            return -2
        elif next_player == history.get_offensive_player():
            return -0.5
        else:
            return 1

    def cfr(self, history, cards, player, p0, p1, p2):

        # determine current player
        current_player = history.get_current_player()

        # determine payout if state is terminal
        if history.is_terminal():
            return history.get_payout(player)

        # get infoset of player and corresponding node
        else:
            #print("Node Map : ", self.node_map.get_infosets())
            private_cards = cards[2 * current_player: 2 * current_player + 2 ]
            infoset = (private_cards, history.mode_proposals, history.cards_played)
            node = self.node_map.get_node(infoset)

            strategy = node.get_strategy()
            #print("node : ", node.infoset, "   regrets:  ", node.cumulative_regrets)
            node_util = 0
            util = [0 for i in range(node.number_of_actions)]

        # for each action: update history, call cfr recursively with updated probabilities
            for action_num in range(node.number_of_actions):

                action = node.actions[action_num]

                new_history = history + action

                if current_player == 0:
                    util[action_num] = self.cfr(new_history, cards, player, strategy[action_num] * p0, p1, p2)
                elif current_player == 1:
                    util[action_num] = self.cfr(new_history, cards, player, p0, strategy[action_num] * p1, p2)
                else:
                    util[action_num] = self.cfr(new_history, cards, player, p0, p1, strategy[action_num] * p2)

                node_util += strategy[action_num] * util[action_num]

        # for each action: compute and update counterfactual regrets

            if current_player == player:
                print(current_player)

                for action_num in range(node.number_of_actions):
                    regret = util[action_num] - node_util
                    print("regret for action {}  :   {}".format(node.actions[action_num], regret))
                    if current_player == 0:
                        counterfactual_probability = p1 * p2
                    elif current_player == 1:
                        counterfactual_probability = p0 * p2
                    else:
                        counterfactual_probability = p0 * p1
                    print("p0, p1, p2 : ", p0, p1, p2)
                    print("cf probability : ", counterfactual_probability)
                    node.cumulative_regrets[action_num] += counterfactual_probability * regret

                print("Node: ", node.infoset, "  strategy : ", node.get_strategy(),
                      " regrets :  ", node.cumulative_regrets, "  node util : ", node_util)

            return node_util

    def train(self, iterations, shuffle=True):
        util0 = 0
        util1 = 0
        util2 = 0
        for i in range(iterations):

            cards = [(1, 0), (2, 1), (2, 0), (3, 0), (1, 1), (3, 1)]  # cards shuffled, dealt -> chance sampling
            if shuffle:
                random.shuffle(cards)

            history = History(mode_proposals=[], cards_played=[], starting_deck=cards)

            util2 += self.cfr(history=history, cards=cards, player=2, p0=1, p1=1, p2=1)
            util1 += self.cfr(history=history, cards=cards, player=1, p0=1, p1=1, p2=1)
            util0 += self.cfr(history=history, cards=cards, player=0, p0=1, p1=1, p2=1)

            for node in self.node_map.get_nodes():
                node.update_strategy()

            if i % 2 == 0:
                print("\n Iteration {}".format(i))
                print("Player 0: Average Game Value : {}\n".format(util0 / iterations))
                print("Player 1: Average Game Value : {}\n".format(util1 / iterations))
                print("Player 2: Average Game Value : {}\n".format(util2 / iterations))
