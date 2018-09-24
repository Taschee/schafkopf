import imageio
from PIL import Image, ImageSequence
from schafkopf.players.mc_tree import MCTree

from schafkopf.players.mc_node import MCNode
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.tournaments.game_states_trick_play import sample_game_states


def make_gif(filenames, duration, outputname):
    images = [imageio.imread(filename) for filename in filenames]
    imageio.mimsave(ims=images, uri=outputname, duration=duration)


def main():
    game_state = sample_game_states[18]

    num_simulations = 100
    ucb_constant = 0.1

    player = UCTPlayer(ucb_const=ucb_constant, num_samples=1, num_simulations=num_simulations)

    root_node = MCNode(game_state=game_state)
    mc_tree = MCTree(root_node=root_node)

    for sim_num in range(1, player.num_simulations + 1):
        selected_node = player.selection(mc_tree)
        rewards = player.simulation(selected_node)
        mc_tree.backup_rewards(leaf_node=selected_node, rewards=rewards)

        mc_tree.visualize_tree(ucb=player.ucb_const,
                               filename="img_{}".format(sim_num))

    filenames = ["img_{}.png".format(i) for i in range(player.num_simulations, 0, -1)]
    gif_name = "Gif_test.gif"
    duration = 0.2
    make_gif(filenames=filenames, outputname=gif_name, duration=duration)

    im = Image.open(gif_name)
    frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
    frames.reverse()
    frames[0].save('reversed.gif', save_all=True, append_images=frames[1:])


if __name__ == "__main__":
    main()
