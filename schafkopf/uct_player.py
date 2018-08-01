from schafkopf.mc_tree import MCTree
from schafkopf.mc_node import MCNode
from schafkopf.helpers import sample_opponent_hands
from schafkopf.players import Player, DummyPlayer, RandomPlayer
from schafkopf.game import Game
from copy import deepcopy
import multiprocessing as mp
import random

class UCTPlayer(Player):

    def __init__(self, name="UCT", ucb_const=100, num_samples=10):
        Player.__init__(self, name=name)
        self.ucb_const = ucb_const
        self.num_samples = num_samples

    def uct_search(self, game_state, num_simulations=100):
        root_node = MCNode(game_state=game_state)
        mc_tree = MCTree(root_node=root_node)

        for sim_num in range(1, num_simulations + 1):
            selected_node = self.selection(mc_tree)
            rewards = self.simulation(selected_node)
            mc_tree.backup_rewards(leaf_node=selected_node, rewards=rewards)

        best_child_node = mc_tree.root_node.best_child(ucb_const=0)
        best_action = best_child_node.previous_action

        return best_action

    def selection(self, mc_tree):
        current_node = mc_tree.root_node
        while not current_node.is_terminal():
            if not current_node.fully_expanded():
                return self.expand(mc_tree=mc_tree, node=current_node)
            else:
                current_node = current_node.best_child(ucb_const=self.ucb_const)
        return current_node

    def expand(self, mc_tree, node):
        not_visited_actions = set(node.game_state["possible_actions"])
        for child in node.children:
            not_visited_actions.remove(child.previous_action)
        chosen_action = random.choice(not_visited_actions)
        new_state = self.get_new_state(game_state=node.game_state,
                                       action=chosen_action)
        new_node = MCNode(parent=node, game_state=new_state)
        mc_tree.add_node(node=new_node,
                         parent_node=node)
        return new_node

    def get_new_state(self, game_state, action):
        playerlist = [DummyPlayer(favorite_mode=action, favorite_cards=[action]),
                      DummyPlayer(favorite_mode=action, favorite_cards=[action]),
                      DummyPlayer(favorite_mode=action, favorite_cards=[action]),
                      DummyPlayer(favorite_mode=action, favorite_cards=[action])]
        game = Game(game_state=game_state, players=playerlist)
        game.next_action()
        return game.get_game_state()

    def simulation(self, selected_node):
        playerlist = [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]
        game = Game(players=playerlist, game_state=selected_node.game_state)
        game.play()
        rewards = game.get_payouts()
        return rewards

    def sample_game_state(self, public_info):

        # sample opponent hands
        player_hands = sample_opponent_hands(tricks=public_info["tricks"],
                                             current_trick=public_info["current_trick"],
                                             trumpcards=public_info["trumpcards"],
                                             playerindex=public_info["current_player_index"],
                                             player_hand=self._hand)

        # add player_hands and possible actions to game state
        game_state = public_info
        game_state["player_hands"] = player_hands
        game = Game(game_state=game_state, players=[RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()])
        game_state["possible_actions"] = game.get_possible_actions()
        return game_state

    def choose_game_mode(self, public_info, options):
        sampled_states = [self.sample_game_state(public_info) for num in range(self.num_samples)]

        num_workers = mp.cpu_count()
        pool = mp.Pool(num_workers)

        # maybe change this to choosing highest average payout/ucb_value? Now: most frequent best action is chosen
        results = pool.map(func=self.uct_search, iterable=sampled_states)

        best_action = max(results, key=results.count)

        return best_action

    def play_card(self, public_info, options=None):
        # choose card by sampling opponent cards N times, in each sample perform MonteCarloSimulation, return best card

        sampled_states = [self.sample_game_state(public_info) for num in range(self.num_samples)]

        num_workers = mp.cpu_count()
        pool = mp.Pool(num_workers)

        # maybe change this to choosing highest average payout/ucb_value? Now: most frequent best action is chosen
        results = pool.map(func=self.uct_search, iterable=sampled_states)

        best_action = max(results, key=results.count)

        return best_action
