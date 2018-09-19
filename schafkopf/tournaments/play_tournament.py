import time
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.players.heuristics_player import HeuristicsPlayer
from schafkopf.players.nn_player import NNPlayer
from schafkopf.tournament import Tournament


def main():
    playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=1),
                  # NNPlayer(game_mode_nn='../players/models/bigger_classifier_sortedhands_lr0.02.hdf5',
                  #          partner_nn='../players/models/partner_model_bigger_1.hdf5',
                  #          solo_nn='../players/models/solo_model_bigger_1.hdf5',
                  #          wenz_nn='../players/models/wenz_model_bigger_1.hdf5'),
                  HeuristicsPlayer(name="B"), HeuristicsPlayer(name="C"), HeuristicsPlayer(name="D")]

    tournament = Tournament(playerlist, number_of_games=100)

    start_time = time.time()
    cum_rew_old = [0, 0, 0, 0]
    while not tournament.finished():
        start_time_game = time.time()
        print('Starting game ', tournament.game_number)
        tournament.play_next_game()
        print('Game took ', time.time() - start_time_game)
        print('Results : ', [tournament.cumulative_rewards[i] - cum_rew_old[i] for i in range(4)])
        cum_rew_old = tournament.cumulative_rewards[:]


    end_time = time.time()

    print("Time : ", end_time - start_time, " seconds")
    print(" Final Results : ", tournament.get_tournament_results())


if __name__ == "__main__":
    main()
