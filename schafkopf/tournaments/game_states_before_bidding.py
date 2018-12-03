import random

import pickle

from schafkopf.card_deck import CardDeck
from schafkopf.game_modes import NO_GAME, WENZ, PARTNER_MODE, SOLO
from schafkopf.suits import SUITS, ACORNS, LEAVES, BELLS


def define_game_state(player_hands, leading_player_index, mode_proposals):
    return {"player_hands": player_hands,
            "leading_player_index": leading_player_index,
            "current_player_index": leading_player_index,
            "declaring_player": 0,
            "game_mode": (NO_GAME, None),
            "mode_proposals": mode_proposals,
            "tricks": [],
            "current_trick": None,
            "possible_actions": [(NO_GAME, None), (WENZ, None)] +
                                [(PARTNER_MODE, suit) for suit in [ACORNS, LEAVES, BELLS]] +
                                [(SOLO, suit) for suit in SUITS]}


def main():
    with open('game_states_before_bidding.p', 'wb') as f:
        for _ in range(100):
            deck = CardDeck()
            player_hands = deck.shuffle_and_deal_hands()

            game_state = define_game_state(player_hands=player_hands,
                                           leading_player_index=random.choice(range(4)),
                                           mode_proposals=[])
            pickle.dump(game_state, f)


if __name__ == '__main__':
    main()
