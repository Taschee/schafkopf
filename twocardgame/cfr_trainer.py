import random
from twocardgame import TwoCardGame
from players import CFRPlayer

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

    def cfr(self, game, p0, p1, p2):

        # if state is terminal, get payout

        if game.finished():
            if game.get_game_mode() is not WEITER:
                playerindex = game.get_tricks()[-1].leading_player_index
                return game.get_payout(playerindex)
            else:
                return 0

        else:
            playerindex = game.get_current_playerindex()
            infoset = game.get_infoset(playerindex)
            node = self.node_map.get_node(infoset)
            strategy = node.get_strategy()
            node_util = 0

            # compute action utilities recursively

            if not game.game_mode_decided():
                possible_actions = [WEITER, SOLO]
                num_actions = 2
                util = [0 for action in range(num_actions)]
                for action in possible_actions:

                    game.next_proposed_game_mode(proposal=action)

                    if playerindex == 0:
                        util[action] = self.adapt_payout(game, playerindex) * self.cfr(game, strategy[action] * p0, p1, p2)
                    elif playerindex == 1:
                        util[action] = self.adapt_payout(game, playerindex) * self.cfr(game, p0, strategy[action] * p1, p2)
                    else:
                        util[action] = self.adapt_payout(game, playerindex) * self.cfr(game, p0, p1, strategy[action] * p2)

                    node_util += strategy[action] * util[action]

                    game.reverse_proposal()

            else:
                hand = infoset["private_cards"]
                possible_actions = game.possible_cards(game.get_current_trick(), hand)
                num_actions = len(possible_actions)
                util = [0 for action in range(num_actions)]
                for action_num in range(num_actions):

                    action = possible_actions[action_num]
                    game.play_next_card(action)

                    if playerindex == 0:
                        util[action_num] = self.adapt_payout(game, playerindex) * self.cfr(game, strategy[action_num] * p0, p1, p2)
                    elif playerindex == 1:
                        util[action_num] = self.adapt_payout(game, playerindex) * self.cfr(game, p0, strategy[action_num] * p1, p2)
                    else:
                        util[action_num] = self.adapt_payout(game, playerindex) * self.cfr(game, p0, p1, strategy[action_num] * p2)

                    node_util += strategy[action_num] * util[action_num]

                    game.reverse_card()

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

        return node_util

    def train(self, iterations):
        util = 0
        for i in range(iterations):
            game = TwoCardGame(self.playerlist)  # cards shuffled, dealt -> chance sampling
            util += self.cfr(game, 1, 1, 1)
            print("Average Game Value : ", util / iterations)



def main():
    player0 = CFRPlayer(name="Player 0")
    player1 = CFRPlayer(name="Player 1")
    player2 = CFRPlayer(name="Player 2")
    cfr_trainer = CFRTrainer(playerlist=[player0, player1, player2])
    cfr_trainer.train(iterations=1)


if __name__ == "__main__":
    main()
