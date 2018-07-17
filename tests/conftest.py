import pytest
from schafkopf.players import DummyPlayer
from schafkopf.suits import LEAVES, ACORNS, BELLS, HEARTS
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.game_modes import NO_GAME, WENZ, PARTNER_MODE, SOLO


@pytest.fixture
def dummy_player_list():
    return [DummyPlayer(name="A",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards=[(OBER, ACORNS), (SEVEN, ACORNS), (ACE, BELLS), (OBER, BELLS),
                                        (UNTER, BELLS), (KING, LEAVES), (TEN, ACORNS), (NINE, ACORNS)]),
            DummyPlayer(name="B",
                        favorite_mode=(PARTNER_MODE, BELLS),
                        favorite_cards=[(ACE, HEARTS), (ACE, ACORNS), (KING, BELLS), (OBER, HEARTS),
                                        (SEVEN, HEARTS), (OBER, LEAVES), (UNTER, ACORNS), (SEVEN, BELLS)]),
            DummyPlayer(name="C",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards=[(KING, HEARTS), (EIGHT, ACORNS), (NINE, BELLS), (TEN, HEARTS),
                                        (UNTER, LEAVES), (TEN, LEAVES), (SEVEN, LEAVES), (KING, ACORNS)]),
            DummyPlayer(name="D",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards=[(EIGHT, HEARTS), (NINE, HEARTS), (EIGHT, BELLS), (UNTER, HEARTS),
                                        (EIGHT, LEAVES), (NINE, LEAVES), (ACE, LEAVES), (TEN, BELLS)])]


@pytest.fixture
def player_hands_before():
    return [[(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (ACE, BELLS),
             (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)],
            [(OBER, LEAVES), (OBER, HEARTS), (UNTER, ACORNS), (ACE, HEARTS),
             (SEVEN, HEARTS), (ACE, ACORNS), (KING, BELLS), (SEVEN, BELLS)],
            [(UNTER, LEAVES), (TEN, LEAVES), (KING, HEARTS), (KING, ACORNS),
             (TEN, HEARTS), (SEVEN, LEAVES), (EIGHT, ACORNS), (NINE, BELLS)],
            [(UNTER, HEARTS), (ACE, LEAVES), (TEN, BELLS), (EIGHT, HEARTS),
             (EIGHT, LEAVES), (EIGHT, BELLS), (NINE, HEARTS), (NINE, LEAVES)]]


@pytest.fixture
def game_state_before_bidding(player_hands_before):
    leading_player = 0
    mode_proposals = []
    game_mode = (NO_GAME, None)
    offensive_players = []
    tricks = []
    current_trick = None
    return {"player_hands": player_hands_before,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}
