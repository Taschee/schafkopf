import random
from copy import deepcopy

from schafkopf.game import Game
from schafkopf.game_modes import PARTNER_MODE, WENZ, SOLO
from schafkopf.helpers import sample_opponent_hands, sample_mode_proposals
from schafkopf.players import DummyPlayer, RandomPlayer
from schafkopf.players.mc_node import MCNode
from schafkopf.players.mc_tree import MCTree
from schafkopf.players.player import Player
from schafkopf.suits import LEAVES, ACORNS, BELLS, HEARTS
from schafkopf.trick import Trick


class UCTPlayer(Player):

    def __init__(self, name="UCT", ucb_const=1, num_samples=10, num_simulations=100, simulation_player_list=None):
        Player.__init__(self, name=name)
        self.simulation_player_list = simulation_player_list
        self.ucb_const = ucb_const
        self.num_samples = num_samples
        self.num_simulations = num_simulations

    def uct_search(self, game_state):
        root_node = MCNode(game_state=game_state)
        mc_tree = MCTree(root_node=root_node)

        for sim_num in range(1, self.num_simulations + 1):
            selected_node = self.selection(mc_tree)
            rewards = self.simulation(selected_node)
            mc_tree.backup_rewards(leaf_node=selected_node, rewards=rewards)

        results = []
        for child in mc_tree.root_node.children:
            results.append((child.previous_action, child.visits, child.get_average_reward(root_node.current_player)))

        return results

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
        chosen_action = random.choice(tuple(not_visited_actions))
        new_state = self.get_new_state(game_state=node.game_state,
                                       action=chosen_action)
        new_node = MCNode(parent=node, game_state=new_state, previous_action=chosen_action)
        mc_tree.add_node(node=new_node,
                         parent_node=node)
        return new_node

    def get_new_state(self, game_state, action):
        playerlist = [DummyPlayer(favorite_mode=action, favorite_cards=[action]),
                      DummyPlayer(favorite_mode=action, favorite_cards=[action]),
                      DummyPlayer(favorite_mode=action, favorite_cards=[action]),
                      DummyPlayer(favorite_mode=action, favorite_cards=[action])]
        game = Game(game_state=deepcopy(game_state), players=playerlist)
        game.next_action()
        return game.get_game_state()

    def simulation(self, selected_node):
        if self.simulation_player_list is None:
            playerlist = [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]
            # if bidding isn't over and >= 2 proposals are made, in simulation uct_player should stick with his proposal
            game = Game(players=playerlist, game_state=selected_node.game_state)
            if not game.bidding_game.finished():
                player_pos = self.get_player_position(selected_node.game_state)
                favorite_mode = selected_node.game_state['mode_proposals'][(player_pos - game.leading_player_index) % 4]
                playerlist[player_pos] = DummyPlayer(favorite_mode=favorite_mode)
        else:
            playerlist = self.simulation_player_list
        # in case the game mode is not yet publicly declared (in bidding phase), take a random suit
        sim_game_state = deepcopy(selected_node.game_state)
        game_type = sim_game_state['game_mode'][0]
        game_suit = sim_game_state['game_mode'][1]
        if game_type == PARTNER_MODE and game_suit is None:
            ran_suit = random.choice([BELLS, ACORNS, LEAVES])
            sim_game_state['game_mode'] = (game_type, ran_suit)
        # if game_type is not known yet, but at least two proposals are made:
        elif game_type > PARTNER_MODE and len(sim_game_state['mode_proposals']) <= 4 \
                and sim_game_state['declaring_player'] != sim_game_state['current_player_index']:
            sim_game_state['game_mode'] = random.choice([(WENZ, None), (SOLO, ACORNS), (SOLO, HEARTS),
                                                         (SOLO, BELLS), (SOLO, LEAVES)])
        game_simulation = Game(players=playerlist, game_state=deepcopy(sim_game_state))
        game_simulation.play()
        rewards = game_simulation.get_payouts()
        return rewards

    def sample_game_state(self, public_info):
        # sample opponent hands
        if public_info["current_trick"] is None:
            current_trick = Trick(leading_player_index=public_info["leading_player_index"])
        else:
            current_trick = public_info["current_trick"]

        player_hands = sample_opponent_hands(tricks=public_info["tricks"],
                                             current_trick=current_trick,
                                             trumpcards=public_info["trumpcards"],
                                             playerindex=public_info["current_player_index"],
                                             player_hand=self.hand)

        # recreate possible mode proposals from public info
        mode_proposals = sample_mode_proposals(public_info)

        # add player_hands and possible actions to game state
        game_state = deepcopy(public_info)
        game_state["mode_proposals"] = mode_proposals
        game_state["player_hands"] = player_hands
        game = Game(game_state=game_state, players=[RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()])
        game_state["possible_actions"] = game.get_possible_actions()

        return game_state

    def choose_game_mode(self, public_info, options):
        if len(options) == 1:
            return list(options)[0]
        else:
            sampled_states = [self.sample_game_state(public_info) for num in range(self.num_samples)]

            move_counts = {move: 0 for move in options}
            move_av_rewards = {move: 0 for move in options}

            for state in sampled_states:
                mc_results = self.uct_search(game_state=state)
                for move, move_count, average_reward in mc_results:
                    move_counts[move] += move_count
                    move_av_rewards[move] += average_reward

            """
            num_workers = mp.cpu_count()
            pool = mp.Pool(num_workers)

            # maybe change this to choosing highest average payout/ucb_value? Now: most frequent best action is chosen
            results = pool.map(func=self.uct_search, iterable=sampled_states)
            """
            best_action = max(move_counts, key=move_counts.get)

            return best_action

    def play_card(self, public_info, options=None):
        # choose card by sampling opponent cards N times, in each sample perform MonteCarloSimulation, return best card
        if len(options) == 1:
            card = list(options)[0]
        else:
            sampled_states = [self.sample_game_state(public_info) for num in range(self.num_samples)]

            move_counts = {move: 0 for move in options}
            move_av_rewards = {move: 0 for move in options}

            for state in sampled_states:
                mc_results = self.uct_search(game_state=state)
                for move, move_count, average_reward in mc_results:
                    move_counts[move] += move_count
                    move_av_rewards[move] += average_reward

            """
            num_workers = mp.cpu_count()
            pool = mp.Pool(num_workers)

            results = pool.map(func=self.uct_search, iterable=sampled_states)
            """

            card = max(move_counts, key=move_counts.get)

        assert card in self.hand, 'Card {} not in hand: {}'.format(card, self.hand)
        self.hand.remove(card)
        return card
