from dataclasses import dataclass
from typing import List, Tuple, Union

from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.game_modes import NO_GAME
from schafkopf.helpers import sort_hand
from schafkopf.players import HeuristicsPlayer, DummyPlayer


@dataclass
class GameResult:
    payouts: Tuple[int, int, int, int]
    winners: List[int]
    declaring_player: Union[int, None]
    game_mode: tuple[int, Union[int, None]]


class SchafkopfGame:
    def __init__(self, leading_player_index):
        self.players = [DummyPlayer(), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()]
        self.game_state = self._new_game_state(leading_player_index)

    def human_players_turn(self):
        return self.game_state["current_player_index"] == 0

    def next_human_bid(self, next_action):
        players = [DummyPlayer(favorite_mode=next_action), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()]
        game = Game(players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        return self.game_state

    def next_human_card(self, next_action):
        players = [DummyPlayer(favorite_cards=[next_action]), HeuristicsPlayer(), HeuristicsPlayer(),
                   HeuristicsPlayer()]
        game = Game(players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        return self.game_state

    def next_action(self):
        game = Game(self.players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        return self.game_state

    def possible_bids(self):
        game = Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        )
        hand = game.playerlist[0].hand
        mode_to_beat = game.bidding_game.mode_to_beat
        possible_modes = list(game.bidding_game.determine_possible_game_modes(hand=hand, mode_to_beat=mode_to_beat))
        possible_modes.sort()
        return possible_modes

    def bidding_is_finished(self):
        return Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        ).bidding_game.finished()

    def finished(self):
        return Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        ).finished()

    def get_results(self) -> GameResult:
        game = Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        )
        if not game.finished():
            raise RuntimeError("No results yet")
        if self.game_state["game_mode"][0] == NO_GAME:
            return GameResult((0, 0, 0, 0), [], None, self.game_state["game_mode"])
        else:
            return GameResult(tuple(game.get_payouts()), game.determine_winners(), game.trick_game.offensive_players,
                              self.game_state["game_mode"])

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
