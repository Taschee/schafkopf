import pytest
from schafkopf.game import Game
from schafkopf.trick import Trick
from schafkopf.suits import BELLS, LEAVES, HEARTS, ACORNS
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.game_modes import PARTNER_MODE, NO_GAME, WENZ,SOLO
from schafkopf.payouts import BASIC_PAYOUT_PARTNER_MODE, BASIC_PAYOUT_SOLO, EXTRA_PAYOUT
from schafkopf.card_deck import CardDeck


@pytest.fixture
def partner_game(partner_player_list, game_state_partner):
    return Game(players=partner_player_list, game_state=game_state_partner)


@pytest.fixture
def wenz_game(wenz_player_list, game_state_wenz):
    return Game(players=wenz_player_list, game_state=game_state_wenz)


@pytest.fixture
def solo_game(solo_player_list, game_state_solo):
    return Game(players=solo_player_list, game_state=game_state_solo)


def test_init_partner_mode(partner_game):
    assert partner_game.leading_player_index == 0
    assert len(partner_game.bidding_game.mode_proposals) == 0
    assert partner_game.trick_game.playerlist[0].get_hand() == [(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS),
                                                                (ACE, BELLS), (KING, LEAVES), (TEN, ACORNS),
                                                                (SEVEN, ACORNS), (NINE, ACORNS)]


def test_play_partner_mode(partner_game):
    assert not partner_game.finished()
    partner_game.play()
    assert partner_game.bidding_game.finished()
    assert partner_game.trick_game.offensive_players == [1, 0]
    assert partner_game.trick_game.finished()
    assert len(partner_game.trick_game.tricks) == 8
    trick = Trick(leading_player_index=1,
                  cards=[(NINE, ACORNS), (SEVEN, BELLS), (KING, ACORNS), (TEN, BELLS)],
                  winner=3,
                  score=14)
    trick.current_player_index = 0
    assert partner_game.trick_game.tricks[-1] == trick


def test_score_offensive_players_partner_mode(partner_game):
    partner_game.play()
    assert partner_game.trick_game.game_mode == (PARTNER_MODE, BELLS)
    assert partner_game.score_offensive_players() == 91


def test_payout_partner_mode(partner_game):
    partner_game.play()
    assert partner_game.trick_game.finished()
    assert partner_game.get_payout(player=0) == BASIC_PAYOUT_PARTNER_MODE + EXTRA_PAYOUT * 6
    assert partner_game.get_payout(player=1) == BASIC_PAYOUT_PARTNER_MODE + EXTRA_PAYOUT * 6
    assert partner_game.get_payout(player=2) == -(BASIC_PAYOUT_PARTNER_MODE + EXTRA_PAYOUT * 6)
    assert partner_game.get_payout(player=3) == -(BASIC_PAYOUT_PARTNER_MODE + EXTRA_PAYOUT * 6)


def test_init_wenz(wenz_game):
    assert wenz_game.leading_player_index == 1
    assert len(wenz_game.bidding_game.mode_proposals) == 0
    assert wenz_game.trick_game.playerlist[0].get_hand() == [(TEN, LEAVES), (OBER, BELLS), (UNTER, BELLS),
                                                             (NINE, LEAVES), (KING, LEAVES), (TEN, ACORNS),
                                                             (EIGHT, ACORNS) , (KING, HEARTS)]


def test_play_wenz(wenz_game):
    assert not wenz_game.finished()
    wenz_game.play()
    assert wenz_game.bidding_game.finished()
    assert wenz_game.bidding_game.game_mode == (WENZ, None)
    assert wenz_game.trick_game.finished()
    assert len(wenz_game.trick_game.tricks) == 8
    trick = Trick(leading_player_index=3,
                  cards=[(KING, LEAVES), (KING, BELLS), (TEN, HEARTS), (NINE, HEARTS)],
                  winner=2,
                  score=18)
    trick.current_player_index = 2
    assert wenz_game.trick_game.tricks[-1] == trick


def test_score_offensive_players_wenz(wenz_game):
    wenz_game.play()
    assert wenz_game.trick_game.game_mode == (WENZ, None)
    assert wenz_game.trick_game.offensive_players == [3]
    assert wenz_game.score_offensive_players() == 89


def test_payout_wenz(wenz_game):
    wenz_game.play()
    assert wenz_game.trick_game.finished()
    assert wenz_game.get_payout(player=0) == -(BASIC_PAYOUT_SOLO + 2 * EXTRA_PAYOUT)
    assert wenz_game.get_payout(player=1) == -(BASIC_PAYOUT_SOLO + 2 * EXTRA_PAYOUT)
    assert wenz_game.get_payout(player=2) == -(BASIC_PAYOUT_SOLO + 2 * EXTRA_PAYOUT)
    assert wenz_game.get_payout(player=3) == 3 * (BASIC_PAYOUT_SOLO + 2 * EXTRA_PAYOUT)


def test_play_solo(solo_game):
    assert not solo_game.finished()
    solo_game.play()
    assert solo_game.bidding_game.finished()
    assert solo_game.bidding_game.game_mode == (SOLO, ACORNS)
    assert solo_game.trick_game.finished()
    assert len(solo_game.trick_game.tricks) == 8
    trick = Trick(leading_player_index=1,
                  cards=[(SEVEN, BELLS), (TEN, BELLS), (NINE, BELLS), (ACE, BELLS)],
                  winner=3,
                  score=21)
    trick.current_player_index = 0
    assert solo_game.trick_game.tricks[2] == trick


def test_score_offensive_players_solo(solo_game):
    solo_game.play()
    assert solo_game.trick_game.game_mode == (SOLO, ACORNS)
    assert solo_game.trick_game.offensive_players == [0]
    assert solo_game.score_offensive_players() == 60


def test_payout_solo(solo_game):
    solo_game.play()
    assert solo_game.trick_game.finished()
    assert solo_game.get_payout(player=0) == -3 * BASIC_PAYOUT_SOLO
    assert solo_game.get_payout(player=1) == BASIC_PAYOUT_SOLO
    assert solo_game.get_payout(player=2) == BASIC_PAYOUT_SOLO
    assert solo_game.get_payout(player=3) == BASIC_PAYOUT_SOLO
