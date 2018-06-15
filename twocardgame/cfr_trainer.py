import random
from twocardgame.twocardgame import TwoCardGame, ThreePlayerTrick
from twocardgame.players import CFRPlayer

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
        for i in range(self.number_of_actions):
            self.cumulative_strategies[i] += weight * strategy[i]
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
            node = self._nodes[index]
        else:
            node = Node(infoset)
            self.add_node(node)
        return node


class CFRTrainer:
    def __init__(self, playerlist):
        self.node_map = NodeMap()
        self.playerlist = playerlist

    def adapt_payout(self, game, player):
        next_player = (player + 1) % 3
        prev_player = (player + 2) % 3
        if game.is_offensive_player(player):
            return -2
        elif game.is_offensive_player(next_player):
            return -0.5
        elif game.is_offensive_player(prev_player):
            return 1
        else:
            return 1


    def cfr(self, history, cards, p0, p1, p2):

        game = TwoCardGame(players=self.playerlist, cards=cards)

        game.prepare_state(history)
        print("\nGame state : \nCurrent player: {}, game mode decided: {}".format(game.get_current_playerindex(),
                                                                                game.game_mode_decided()))

        print("\nCFR : current player : {},  game mode : {}".format(game.get_current_playerindex(), game.get_game_mode()))
        print("Tricks : ", [trick.cards for trick in game.get_tricks()])
        print("Current trick: ", game.get_current_trick().cards)
        # if state is terminal, get payout
        print(" Game Finished : ", game.finished())

        if game.finished():

            if game.get_game_mode() is not WEITER:
                playerindex = game.get_tricks()[-1].leading_player_index
                print( "FINISHED, player", playerindex)
                payout = game.get_payout(playerindex)
            else:
                print(" FINISHED: Weiter")
                payout = 0
            print("utility : ", payout)
            return payout

        else:

            playerindex = game.get_current_playerindex()
            print("current player : ", playerindex)
            infoset = game.get_infoset(playerindex)

            node = self.node_map.get_node(infoset)
            print("New Node : ", node.infoset)
            print("NodeMap:", self.node_map._infosets)
            strategy = node.get_strategy()
            node_util = 0

            # compute action utilities recursively

            if not game.game_mode_decided():
                possible_actions = [WEITER, SOLO]
                num_actions = 2
                util = [0 for action in range(num_actions)]
                for action in possible_actions:

                    print(" Action : ", action)
                    game.next_proposed_game_mode(proposal=action)
                    print(" history: ", history)
                    new_history = game.get_history()
                    print(" new history: ", new_history)

                    if playerindex == 0:
                        util[action] = self.adapt_payout(game, playerindex) * \
                                       self.cfr(new_history, cards, strategy[action] * p0, p1, p2)
                    elif playerindex == 1:
                        util[action] = self.adapt_payout(game, playerindex) * \
                                       self.cfr(new_history, cards, p0, strategy[action] * p1, p2)
                    else:
                        util[action] = self.adapt_payout(game, playerindex) * \
                                       self.cfr(new_history, cards, p0, p1, strategy[action] * p2)

                    node_util += strategy[action] * util[action]

            else:
                hand = game.get_current_player().get_hand()
                possible_actions = game.possible_cards(game.get_current_trick(), hand)
                num_actions = len(possible_actions)
                util = [0 for action in possible_actions]
                for action_num in range(num_actions):

                    print("possible actions : ", possible_actions)

                    action = possible_actions[action_num]
                    print(" Action : ", action)
                    game.play_next_card(action)
                    game.trick_finished()
                    new_history = game.get_history()

                    if playerindex == 0:
                        util[action_num] = self.adapt_payout(game, playerindex) * \
                                           self.cfr(new_history, cards, strategy[action_num] * p0, p1, p2)
                    elif playerindex == 1:
                        util[action_num] = self.adapt_payout(game, playerindex) * \
                                           self.cfr(new_history, cards, p0, strategy[action_num] * p1, p2)
                    else:
                        util[action_num] = self.adapt_payout(game, playerindex) * \
                                           self.cfr(new_history, cards, p0, p1, strategy[action_num] * p2)

                    node_util += strategy[action_num] * util[action_num]

            # compute counterfactual regrets

            for i in range(num_actions):
                regret = util[i] - node_util
                if playerindex == 0:
                    counterfactual_probability = p1 * p2
                elif playerindex == 1:
                    counterfactual_probability = p0 * p2
                else:
                    counterfactual_probability = p0 * p1
                node.cumulative_regrets[i] += counterfactual_probability * regret

            print("utility : ", node_util)
            print("Infoset later:", infoset)

            return node_util

    def train(self, iterations):
        util = 0
        for i in range(iterations):

            cards = [(3, 0), (2, 0), (1, 0), (1, 1), (2, 1), (3, 1)]  # cards shuffled, dealt -> chance sampling
            random.shuffle(cards)

            history = {"game_mode": 0,
            "mode_proposals": [None, None, None],
            "deciding_players": set(self.playerlist),
            "offensive_players": [],
            "tricks": [],
            "current_trick": ThreePlayerTrick(self.playerlist, leading_player=0),
            "current_player_index": 0}

            util += self.cfr(history, cards, 1, 1, 1)
            print("\n Iteration {}   Average Game Value : {}\n".format(i, util / iterations))
