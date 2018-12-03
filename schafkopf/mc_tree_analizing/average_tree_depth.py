import random

from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.players.mc_tree import MCTree
from schafkopf.players.mc_node import MCNode
from schafkopf.players.nn_player import NNPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.card_deck import CardDeck
from schafkopf.suits import SUITS, ACORNS, LEAVES, BELLS
from schafkopf.tournaments.game_states_trick_play import sample_game_states


def new_game_state():
    deck = CardDeck()
    player_hands = deck.shuffle_and_deal_hands()
    leading_player_index = random.choice(range(4))
    return {"player_hands": player_hands,
            "leading_player_index": leading_player_index,
            "current_player_index": leading_player_index,
            "declaring_player": 0,
            "game_mode": (NO_GAME, None),
            "mode_proposals": [],
            "tricks": [],
            "current_trick": None,
            "possible_actions": [(NO_GAME, None), (WENZ, None)] +
                                [(PARTNER_MODE, suit) for suit in [ACORNS, LEAVES, BELLS]] +
                                [(SOLO, suit) for suit in SUITS]}

def main():
    sim_player_list = [NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                                partner_nn='../players/models/partner_model_wider_data_2.hdf5',
                                solo_nn='../players/models/solo_model_wider_data_10.hdf5',
                                wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
                       NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                                partner_nn='../players/models/partner_model_wider_data_2.hdf5',
                                solo_nn='../players/models/solo_model_wider_data_10.hdf5',
                                wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
                       NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                                partner_nn='../players/models/partner_model_wider_data_2.hdf5',
                                solo_nn='../players/models/solo_model_wider_data_10.hdf5',
                                wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
                       NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                                partner_nn='../players/models/partner_model_wider_data_2.hdf5',
                                solo_nn='../players/models/solo_model_wider_data_10.hdf5',
                                wenz_nn='../players/models/wenz_model_wider_data_10.hdf5')]

    cum_depth = 0
    for game_state in sample_game_states:

        num_simulations = 100
        ucb_constant = 0.1

        player = UCTPlayer(ucb_const=ucb_constant,
                           num_samples=1,
                           num_simulations=num_simulations,
                           simulation_player_list=None)

        root_node = MCNode(game_state=game_state)
        mc_tree = MCTree(root_node=root_node)

        for sim_num in range(1, player.num_simulations + 1):
            selected_node = player.selection(mc_tree)
            rewards = player.simulation(selected_node)
            mc_tree.backup_rewards(leaf_node=selected_node, rewards=rewards)

        depth = mc_tree.max_depth()
        cum_depth += depth

    print('Average tree depth without NN:', cum_depth / len(sample_game_states) )

    cum_depth_with_nn = 0
    for game_state in sample_game_states:

        num_simulations = 100
        ucb_constant = 0.1

        player = UCTPlayer(ucb_const=ucb_constant,
                           num_samples=1,
                           num_simulations=num_simulations,
                           simulation_player_list=sim_player_list)

        root_node = MCNode(game_state=game_state)
        mc_tree = MCTree(root_node=root_node)

        for sim_num in range(1, player.num_simulations + 1):
            selected_node = player.selection(mc_tree)
            rewards = player.simulation(selected_node)
            mc_tree.backup_rewards(leaf_node=selected_node, rewards=rewards)

        depth = mc_tree.max_depth()
        cum_depth_with_nn += depth

    print('Average tree depth with NN:', cum_depth_with_nn / len(sample_game_states))


if __name__ == "__main__":
    main()
