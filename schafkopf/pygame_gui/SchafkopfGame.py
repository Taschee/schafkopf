import pygame

from schafkopf.card_deck import CardDeck
from schafkopf.game_modes import NO_GAME
from schafkopf.helpers import sort_hand


class SchafkopfGame:
    def __init__(self, leading_player_index):
        self.game_state = self._new_game_state(leading_player_index)

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(self.game_state)

    def _new_game_state(self, leading_player_index):
        game_state = {
            'player_hands': [sort_hand(h) for h in self._random_player_hands()],
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

    @staticmethod
    def _random_player_hands():
        return CardDeck().shuffle_and_deal_hands()
