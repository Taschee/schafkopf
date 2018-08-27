import time
from schafkopf.game import Game
import schafkopf.game_states_trick_play
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.players.heuristics_player import HeuristicsPlayer


#####     DONT DO IT WITH MULTIPROCESSING!  :P - not sure why


playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=0.1),
              HeuristicsPlayer(name="B"),
              HeuristicsPlayer(name="C"),
              HeuristicsPlayer(name="D")]

def main():

    tournament_game_states = schafkopf.game_states_trick_play.sample_game_states[:20]

    total_scores = [0, 0, 0, 0]

    for num in range(len(tournament_game_states)):
        start_time = time.time()
        game_state = tournament_game_states[num]
        game = Game(game_state=game_state, players=playerlist)
        game.play()
        rewards = game.get_payouts()
        for i in range(4):
            total_scores[i] += rewards[i]
        end_time = time.time()
        print("Game {} took {} seconds".format(num + 1, end_time - start_time))
        print("Rewards : ", rewards)

    print("Final scores : ", total_scores)


if __name__ == "__main__":
    main()
