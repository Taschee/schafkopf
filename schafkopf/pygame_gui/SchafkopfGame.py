from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.game_modes import NO_GAME
from schafkopf.helpers import sort_hand
from schafkopf.players import HeuristicsPlayer, DummyPlayer


class SchafkopfGame:
    def __init__(self, leading_player_index):
        self.game_state = self._new_game_state(leading_player_index)

    def next_bidding_action(self, next_action):
        players = [DummyPlayer(favorite_mode=next_action), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()]
        game = Game(players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        return self.game_state

    def next_action(self, next_action):
        players = [
            DummyPlayer(favorite_cards=[next_action]), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()
        ]
        game = Game(players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        return self.game_state

    def possible_actions(self):
        return Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        ).get_possible_actions()

    def bidding_is_finished(self):
        return Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        ).bidding_game.finished()

    def finished(self):
        return Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        ).finished()

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
