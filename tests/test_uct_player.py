import pytest

from schafkopf.game import Game
from schafkopf.game_modes import PARTNER_MODE, NO_GAME
from schafkopf.players.uct_player import UCTPlayer
from schafkopf.players.random_player import RandomPlayer
from schafkopf.ranks import OBER, UNTER, KING, ACE, SEVEN, NINE, TEN
from schafkopf.suits import ACORNS, BELLS, LEAVES


@pytest.fixture
def uct_playerlist():
    return [UCTPlayer(ucb_const=100, num_samples=10, name="A"),
            UCTPlayer(ucb_const=100, num_samples=10, name="A"),
            UCTPlayer(ucb_const=100, num_samples=10, name="A"),
            UCTPlayer(ucb_const=100, num_samples=10, name="A")]

@pytest.fixture
def game_state_after_bidding(player_hands_partner):
    leading_player = 0
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, BELLS), (NO_GAME, None), (NO_GAME, None)]
    game_mode = (PARTNER_MODE, BELLS)
    current_player = 0
    declaring_player = 1
    tricks = []
    current_trick = None
    possible_actions = [(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (ACE, BELLS),
                        (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)]
    return {"player_hands": player_hands_partner,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "current_player": current_player,
            "declaring_player": declaring_player,
            "tricks": tricks,
            "current_trick": current_trick,
            "possible_actions": possible_actions}


def test_playing(game_state_after_bidding, uct_playerlist):
    game = Game(game_state=game_state_after_bidding, players=uct_playerlist)
