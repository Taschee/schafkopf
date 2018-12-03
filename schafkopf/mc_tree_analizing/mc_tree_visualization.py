from schafkopf.players.mc_tree import MCTree

from schafkopf.players.mc_node import MCNode
from schafkopf.players.nn_player import NNPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.tournaments.game_states_trick_play import sample_game_states


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

    game_state = sample_game_states[15]

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

    mc_tree.visualize_tree(ucb=player.ucb_const,
                           filename="Tree_{}nodes{}ucb_const{}game_mode".format(num_simulations,
                                                                                ucb_constant,
                                                                                game_state["game_mode"]))

if __name__ == "__main__":
    main()
