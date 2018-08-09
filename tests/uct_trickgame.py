import time

from schafkopf.game import Game
from schafkopf.game_states_trick_play import sample_game_states
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.uct_player import UCTPlayer

playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=10),
              RandomPlayer(name="B"), RandomPlayer(name="C"), RandomPlayer(name="D")]

game_state = sample_game_states[0]

def main():
    game = Game(game_state=game_state, players=playerlist)

    start_time = time.time()

    while not game.trick_game.finished():
        game.trick_game.play_next_card()
        print(game.trick_game.current_trick)
        game.trick_game.trick_finished()

    end_time = time.time()

    print("Time: ", end_time - start_time)
    print(game.get_payouts())



if __name__ == "__main__":
    main()
