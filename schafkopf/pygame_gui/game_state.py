from schafkopf.card_deck import CardDeck
from schafkopf.game_modes import NO_GAME


def random_player_hands(card_deck: CardDeck):
    return card_deck.shuffle_and_deal_hands()


def new_game_state(card_deck, leading_player_index):
    game_state = {
        'player_hands': card_deck.shuffle_and_deal_hands(),
        'leading_player_index': leading_player_index,
        'current_player_index': leading_player_index,
        'mode_proposals': [],
        'game_mode': (NO_GAME, None),
        'trumpcards': [],
        'declaring_player': None,
        'tricks': [],
        'current_trick': None
    }
    return game_state
