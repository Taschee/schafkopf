import time

import schafkopf.tournaments.game_states_trick_play
from schafkopf.game import Game
from schafkopf.players.heuristics_player import HeuristicsPlayer
from schafkopf.players.isuct_player import ISUCTPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.nn_player import NNPlayer


sim_player_list = [NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                            partner_nn='../players/models/trickplay_model_partner_extended.hdf5',
                            solo_nn='../players/models/trickplay_model_solo_extended.hdf5',
                            wenz_nn='../players/models/trickplay_model_wenz_extended.hdf5'),
                   NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                            partner_nn='../players/models/trickplay_model_partner_extended.hdf5',
                            solo_nn='../players/models/trickplay_model_solo_extended.hdf5',
                            wenz_nn='../players/models/trickplay_model_wenz_extended.hdf5'),
                   NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                            partner_nn='../players/models/trickplay_model_partner_extended.hdf5',
                            solo_nn='../players/models/trickplay_model_solo_extended.hdf5',
                            wenz_nn='../players/models/trickplay_model_wenz_extended.hdf5'),
                   NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                            partner_nn='../players/models/trickplay_model_partner_extended.hdf5',
                            solo_nn='../players/models/trickplay_model_solo_extended.hdf5',
                            wenz_nn='../players/models/trickplay_model_wenz_extended.hdf5')]


playerlist = [UCTPlayer(num_samples=10, num_simulations=20, ucb_const=1, simulation_player_list=sim_player_list),
              # UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=1),
              # NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
              #          partner_nn='../players/models/trickplay_model_partner_extended.hdf5',
              #          solo_nn='../players/models/trickplay_model_solo_extended.hdf5',
              #          wenz_nn='../players/models/trickplay_model_wenz_extended.hdf5',
              #          use_extended_models=True),
              # HeuristicsPlayer(),
              # RandomPlayer(),
              # ISUCTPlayer(num_simulations=1000, ucb_const=2, simulation_player_list=None),
              HeuristicsPlayer(name="B"),
              HeuristicsPlayer(name="C"),
              HeuristicsPlayer(name="D")]

def main():

    tournament_game_states = schafkopf.tournaments.game_states_trick_play.sample_game_states[:40]
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
