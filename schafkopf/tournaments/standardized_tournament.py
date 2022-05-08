#!/usr/bin/env python3
from schafkopf.game import Game
from schafkopf.players.nn_player import NNPlayer
from schafkopf.players import HeuristicsPlayer, UCTPlayer
import pickle


def play_standardized_tournament(playerlist):
    total_rewards = [0, 0, 0, 0]

    with open('game_states_before_bidding.p', 'rb') as f:

        for game_num in range(1, 101):
            print('-------  Starting game {}  ------'.format(game_num))
            gamestate = pickle.load(f)

            # play each game four times, in a way that each player had every hand once
            for i in range(4):
                print('Round ', i)
                permuted_playerlist = playerlist[i:4] + playerlist[:i]
                game = Game(players=permuted_playerlist, game_state=gamestate)
                game.play()
                payouts = game.get_payouts()
                print('Game mode : ', game.bidding_game.game_mode)
                print('Offensive players : ', [(pl - i) % 4 for pl in game.bidding_game.offensive_players])
                print('Payouts : ', [payouts[(pl - i) % 4] for pl in range(4)])
                for j in range(4):
                    total_rewards[j] += payouts[(j - i) % 4]

        print('\n Final Results : ', total_rewards)


def main():
    # sim_player_list = [NNPlayer(game_mode_nn='../players/models/bigger_classifier_sortedhands_lr0.02.hdf5',
    #                             partner_nn='../players/models/partner_model_wider_data_2.hdf5',
    #                             solo_nn='../players/models/solo_model_wider_data_10.hdf5',
    #                             wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
    #                    NNPlayer(game_mode_nn='../players/models/bigger_classifier_sortedhands_lr0.02.hdf5',
    #                             partner_nn='../players/models/partner_model_wider_data_2.hdf5',
    #                             solo_nn='../players/models/solo_model_wider_data_10.hdf5',
    #                             wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
    #                    NNPlayer(game_mode_nn='../players/models/bigger_classifier_sortedhands_lr0.02.hdf5',
    #                             partner_nn='../players/models/partner_model_wider_data_2.hdf5',
    #                             solo_nn='../players/models/solo_model_wider_data_10.hdf5',
    #                             wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
    #                    NNPlayer(game_mode_nn='../players/models/bigger_classifier_sortedhands_lr0.02.hdf5',
    #                             partner_nn='../players/models/partner_model_wider_data_2.hdf5',
    #                             solo_nn='../players/models/solo_model_wider_data_10.hdf5',
    #                             wenz_nn='../players/models/wenz_model_wider_data_10.hdf5')]

    playerlist = [  # UCTPlayer(num_samples=10, num_simulations=10, ucb_const=1, simulation_player_list=None),
        # UCTPlayer(name="A", num_samples=10, num_simulations=100, ucb_const=1),
        NNPlayer(game_mode_nn='../players/models/bigger_classifier200.hdf5',
                 partner_nn='../players/models/partner_model_wider_data_2.hdf5',
                 solo_nn='../players/models/solo_model_wider_data_10.hdf5',
                 wenz_nn='../players/models/wenz_model_wider_data_10.hdf5'),
        # HeuristicsPlayer(),
        # RandomPlayer(),
        HeuristicsPlayer(name="B"),
        HeuristicsPlayer(name="C"),
        HeuristicsPlayer(name="D")]
    play_standardized_tournament(playerlist)


if __name__ == '__main__':
    main()
