from schafkopf.players.uct_player import UCTPlayer
from schafkopf.players.random_player import RandomPlayer
from schafkopf.game import Game
from schafkopf.game_states_trick_play import sample_game_states


def main():
    state = sample_game_states[10]
    playerlist = [UCTPlayer(ucb_const=0, num_samples=1, num_simulations=1000, visualize=True),
                  RandomPlayer(), RandomPlayer(), RandomPlayer()]
    game = Game(players=playerlist, game_state=state)

    game.next_action()


if __name__ == "__main__":
    main()