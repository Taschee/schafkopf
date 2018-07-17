import pytest
from schafkopf.players import DummyPlayer
from schafkopf.suits import LEAVES, ACORNS, BELLS, HEARTS
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.game_modes import NO_GAME, WENZ, PARTNER_MODE, SOLO


@pytest.fixture
def player_hands_partner():
    return [[(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (ACE, BELLS),
             (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)],
            [(OBER, LEAVES), (OBER, HEARTS), (UNTER, ACORNS), (ACE, HEARTS),
             (SEVEN, HEARTS), (ACE, ACORNS), (KING, BELLS), (SEVEN, BELLS)],
            [(UNTER, LEAVES), (TEN, LEAVES), (KING, HEARTS), (KING, ACORNS),
             (TEN, HEARTS), (SEVEN, LEAVES), (EIGHT, ACORNS), (NINE, BELLS)],
            [(UNTER, HEARTS), (ACE, LEAVES), (TEN, BELLS), (EIGHT, HEARTS),
             (EIGHT, LEAVES), (EIGHT, BELLS), (NINE, HEARTS), (NINE, LEAVES)]]


@pytest.fixture
def partner_player_list():
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
def game_state_partner(player_hands_partner):
    leading_player = 0
    mode_proposals = []
    game_mode = (NO_GAME, None)
    offensive_players = []
    tricks = []
    current_trick = None
    return {"player_hands": player_hands_partner,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}


@pytest.fixture
def player_hands_wenz():
    return [[(TEN, LEAVES), (OBER, BELLS), (UNTER, BELLS), (NINE, LEAVES),
             (KING, LEAVES), (TEN, ACORNS),(EIGHT, ACORNS) , (KING, HEARTS)],
            [(OBER, LEAVES), (SEVEN, ACORNS), (EIGHT, HEARTS), (EIGHT, BELLS),
             (SEVEN, HEARTS), (ACE, ACORNS), (KING, BELLS), (SEVEN, BELLS)],
            [(SEVEN, LEAVES), (OBER, ACORNS), (NINE, ACORNS), (KING, ACORNS),
             (TEN, HEARTS), (UNTER, HEARTS), (OBER, HEARTS), (NINE, BELLS)],
            [(UNTER, LEAVES), (ACE, LEAVES), (TEN, BELLS), (UNTER, ACORNS),
             (EIGHT, LEAVES), (ACE, HEARTS), (NINE, HEARTS), (ACE, BELLS)]]


@pytest.fixture
def wenz_player_list():
    return [DummyPlayer(name="A",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards=[(OBER, BELLS), (UNTER, BELLS), (TEN, LEAVES), (TEN, ACORNS),
                                        (EIGHT, ACORNS), (KING, HEARTS), (NINE, LEAVES), (KING, LEAVES)]),
            DummyPlayer(name="B",
                        favorite_mode=(PARTNER_MODE, BELLS),
                        favorite_cards=[(EIGHT, BELLS), (EIGHT, HEARTS), (OBER, LEAVES), (ACE, ACORNS),
                                        (SEVEN, BELLS) , (SEVEN, HEARTS), (SEVEN, ACORNS), (KING, BELLS)]),
            DummyPlayer(name="C",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards=[(NINE, BELLS), (UNTER, HEARTS), (SEVEN, LEAVES), (NINE, ACORNS),
                                        (OBER, ACORNS), (OBER, HEARTS), (KING, ACORNS), (TEN, HEARTS)]),
            DummyPlayer(name="D",
                        favorite_mode=(WENZ, None),
                        favorite_cards=[(ACE, BELLS), (UNTER, LEAVES), (EIGHT, LEAVES), (UNTER, ACORNS),
                                        (TEN, BELLS), (ACE, HEARTS), (ACE, LEAVES), (NINE, HEARTS)])]


@pytest.fixture
def game_state_wenz(player_hands_wenz):
    leading_player = 1
    mode_proposals = []
    game_mode = (NO_GAME, None)
    offensive_players = []
    tricks = []
    current_trick = None
    return {"player_hands": player_hands_wenz,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}


@pytest.fixture
def player_hands_solo():
    return [[(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (SEVEN, BELLS),
             (OBER, HEARTS), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)],
            [(KING, LEAVES), (OBER, LEAVES), (UNTER, ACORNS), (ACE, HEARTS),
             (SEVEN, LEAVES), (ACE, ACORNS), (EIGHT, ACORNS), (TEN, BELLS)],
            [(EIGHT, LEAVES), (SEVEN, HEARTS), (KING, HEARTS), (KING, ACORNS),
             (TEN, HEARTS), (TEN, LEAVES), (NINE, BELLS), (NINE, HEARTS)],
            [(UNTER, HEARTS), (ACE, LEAVES), (ACE, BELLS), (EIGHT, HEARTS),
             (UNTER, LEAVES), (EIGHT, BELLS), (KING, BELLS), (NINE, LEAVES)]]


@pytest.fixture
def solo_player_list():
    return [DummyPlayer(name="A",
                        favorite_mode=(SOLO, ACORNS),
                        favorite_cards=[(OBER, ACORNS), (OBER, HEARTS), (SEVEN, BELLS), (UNTER, BELLS),
                                        (OBER, BELLS), (SEVEN, ACORNS), (TEN, ACORNS), (NINE, ACORNS)]),
            DummyPlayer(name="B",
                        favorite_mode=(PARTNER_MODE, BELLS),
                        favorite_cards=[(EIGHT, ACORNS), (OBER, LEAVES), (TEN, BELLS), (SEVEN, LEAVES),
                                        (UNTER, ACORNS), (ACE, ACORNS), (KING, LEAVES), (ACE, HEARTS)]),
            DummyPlayer(name="C",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards=[(KING, ACORNS), (TEN, HEARTS), (NINE, BELLS), (EIGHT, LEAVES),
                                        (SEVEN, HEARTS), (TEN, LEAVES), (NINE, HEARTS), (KING, HEARTS)]),
            DummyPlayer(name="D",
                        favorite_mode=(NO_GAME, None),
                        favorite_cards= [(UNTER, HEARTS), (UNTER, LEAVES), (ACE, BELLS), (ACE, LEAVES),
                                         (EIGHT, HEARTS), (EIGHT, BELLS), (KING, BELLS), (NINE, LEAVES)])]


@pytest.fixture
def game_state_solo(player_hands_solo):
    leading_player = 0
    mode_proposals = []
    game_mode = (NO_GAME, None)
    offensive_players = []
    tricks = []
    current_trick = None
    return {"player_hands": player_hands_solo,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}
