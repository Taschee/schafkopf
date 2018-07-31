from schafkopf.uct_player import UCTPlayer
from schafkopf.game_modes import PARTNER_MODE, NO_GAME, SOLO, WENZ
from schafkopf.suits import ACORNS, BELLS, HEARTS, LEAVES
from schafkopf.game import Game
import pytest

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
    offensive_players = [1, 0]
    tricks = []
    current_trick = None
    return {"player_hands": player_hands_partner,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "current_player": current_player,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}
