from schafkopf.players.uct_player import UCTPlayer
from schafkopf.mc_node import MCNode
from schafkopf.mc_tree import MCTree
from schafkopf.game_states_trick_play import sample_game_states


def main():
    game_state = sample_game_states[10]
    player = UCTPlayer(ucb_const=0, num_samples=1, num_simulations=100)

    root_node = MCNode(game_state=game_state)
    mc_tree = MCTree(root_node=root_node)

    for sim_num in range(1, player.num_simulations + 1):
        selected_node = player.selection(mc_tree)
        rewards = player.simulation(selected_node)
        mc_tree.backup_rewards(leaf_node=selected_node, rewards=rewards)

    mc_tree.visualize_tree(ucb=player.ucb_const, filename="Try")


if __name__ == "__main__":
    main()