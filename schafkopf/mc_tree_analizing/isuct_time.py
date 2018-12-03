from schafkopf.players import RandomPlayer
from schafkopf.players.isuct_player import ISUCTPlayer
from schafkopf.ranks import *
from schafkopf.suits import *
from schafkopf.game_modes import *
import time
from schafkopf.game import Game

playerlist = [ISUCTPlayer(name="A", num_simulations=100, simulation_player_list=None, ucb_const=2),
              RandomPlayer(name="B"),
              RandomPlayer(name="C"),
              RandomPlayer(name="D")]


player_hands_partner = [[(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (ACE, BELLS),
                         (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)],
                        [(OBER, LEAVES), (OBER, HEARTS), (UNTER, ACORNS), (ACE, HEARTS),
                         (SEVEN, HEARTS), (ACE, ACORNS), (KING, BELLS), (SEVEN, BELLS)],
                        [(UNTER, LEAVES), (TEN, LEAVES), (KING, HEARTS), (KING, ACORNS),
                         (TEN, HEARTS), (SEVEN, LEAVES), (EIGHT, ACORNS), (NINE, BELLS)],
                        [(UNTER, HEARTS), (ACE, LEAVES), (TEN, BELLS), (EIGHT, HEARTS),
                         (EIGHT, LEAVES), (EIGHT, BELLS), (NINE, HEARTS), (NINE, LEAVES)]]


leading_player = 0
mode_proposals = [(NO_GAME, None), (PARTNER_MODE, BELLS), (NO_GAME, None), (NO_GAME, None)]
game_mode = (PARTNER_MODE, BELLS)
current_player = 0
declaring_player = 1
tricks = []
current_trick = None
possible_actions = [(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (ACE, BELLS),
                        (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)]
game_state_after_bidding = {"player_hands": player_hands_partner,
                            "leading_player_index": leading_player,
                            "mode_proposals": mode_proposals,
                            "game_mode": game_mode,
                            "current_player": current_player,
                            "declaring_player": declaring_player,
                            "tricks": tricks,
                            "current_trick": current_trick,
                            "possible_actions": possible_actions}

def main():
    game = Game(game_state=game_state_after_bidding, players=playerlist)
    public_info = game.get_public_info()
    current_player = game.trick_game.get_current_player()

    start_time = time.time()

    print('Start !')

    actions = current_player.isuct_search(public_info=public_info)
    end_time = time.time()


    print("possible actions : ", game.get_possible_actions())
    print("Best action", actions)
    print("Simulation took {} seconds".format(end_time - start_time))

if __name__ == "__main__":
    main()
