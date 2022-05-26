from typing import List, Tuple, Union

from schafkopf.card_deck import CardDeck
from schafkopf.game import Game
from schafkopf.game_modes import NO_GAME
from schafkopf.helpers import sort_hand
from schafkopf.players import HeuristicsPlayer, DummyPlayer
from schafkopf.pygame_gui.GameResult import GameResult
from schafkopf.trick import Trick


class SchafkopfGame:
    def __init__(self, leading_player_index):
        self.players = [DummyPlayer(), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()]
        self.game_state = self._new_game_state(leading_player_index)
        self.paused_on_last_trick = False

    def human_players_turn(self) -> bool:
        return self.game_state["current_player_index"] == 0

    def no_cards_in_current_trick(self) -> bool:
        current_trick = self.game_state["current_trick"]
        if current_trick is None:
            return True
        else:
            return len([c for c in current_trick.cards if c is not None]) == 0

    def get_player_hand(self) -> List[Tuple[int, int]]:
        return self.game_state["player_hands"][0]

    def get_mode_proposals(self) -> List[Tuple[int, Union[int, None]]]:
        return self.game_state["mode_proposals"]

    def get_declaring_player(self) -> Union[int, None]:
        return self.game_state["declaring_player"]

    def get_game_mode(self) -> Tuple[int, Union[int, None]]:
        return self.game_state["game_mode"]

    def get_opponent_hands(self) -> List[List[Tuple[int, int]]]:
        return self.game_state["player_hands"][1:4]

    def get_current_trick(self) -> List[Union[Tuple[int, int], None]]:
        current_trick: Union[Trick, None] = self.game_state["current_trick"]
        if current_trick is not None:
            return current_trick.cards
        else:
            return []

    def at_least_one_previous_trick(self) -> bool:
        return len(self.game_state["tricks"]) > 0

    def pause(self):
        self.paused_on_last_trick = True

    def unpause(self):
        self.paused_on_last_trick = False

    def next_human_bid(self, next_action):
        players = [DummyPlayer(favorite_mode=next_action), HeuristicsPlayer(), HeuristicsPlayer(), HeuristicsPlayer()]
        game = Game(players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        return self.game_state

    def next_human_card(self, next_action):
        if not self.game_state["current_player_index"] == 0:
            raise ValueError("Not human players turn")
        possible_cards = self.possible_cards()
        if next_action in possible_cards:
            players = [DummyPlayer(favorite_cards=[next_action]), HeuristicsPlayer(), HeuristicsPlayer(),
                       HeuristicsPlayer()]
            game = Game(players, self.game_state)
            game.next_action()
            self.game_state = game.get_game_state()
            if self.at_least_one_previous_trick() and self.no_cards_in_current_trick():
                self.pause()
        return self.game_state

    def next_action(self):
        game = Game(self.players, self.game_state)
        game.next_action()
        self.game_state = game.get_game_state()
        if self.at_least_one_previous_trick() and self.no_cards_in_current_trick():
            self.pause()
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

    def possible_cards(self):
        game = Game(
            [DummyPlayer(), DummyPlayer(), DummyPlayer(), DummyPlayer()], self.game_state
        )
        hand = game.playerlist[0].hand
        current_trick = self.game_state["current_trick"]
        return game.trick_game.possible_cards(current_trick, hand)

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
            return GameResult(
                payouts=(0, 0, 0, 0),
                winners=[],
                declaring_player=None,
                game_mode=self.game_state["game_mode"],
                offensive_players=[],
                offensive_points=0
            )
        else:
            return GameResult(
                payouts=tuple(game.get_payouts()),
                winners=game.determine_winners(),
                declaring_player=self.game_state["declaring_player"],
                game_mode=self.game_state["game_mode"],
                offensive_players=game.trick_game.offensive_players,
                offensive_points=game.score_offensive_players()
            )

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
