import time

from schafkopf.game import Game
from schafkopf.game_modes import NO_GAME, PARTNER_MODE
from schafkopf.players.random_player import RandomPlayer
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.ranks import *
from schafkopf.suits import *

playerlist = [UCTPlayer(name="A", num_samples=10, num_simulations=1000),
              RandomPlayer(name="B"), RandomPlayer(name="C"), RandomPlayer(name="D")]


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

    game_state = current_player.sample_game_state(public_info)

    start_time = time.time()
    best_action = current_player.uct_search(game_state=game_state)
    end_time = time.time()


    print("possible actions : ", game.get_possible_actions())
    print("Best action", best_action)
    print("Simulation took {} seconds".format(end_time - start_time))

if __name__ == "__main__":
    main()
