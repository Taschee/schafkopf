import pytest
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.suits import BELLS, ACORNS, LEAVES, HEARTS, SUITS
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.bidding_game import BiddingGame
from schafkopf.players.dummy_player import DummyPlayer


@pytest.fixture
def dummy_player_list():
    return [DummyPlayer(name="A",
                        favorite_mode=(NO_GAME, None)),
            DummyPlayer(name="B",
                        favorite_mode=(PARTNER_MODE, BELLS)),
            DummyPlayer(name="C",
                        favorite_mode=(NO_GAME, None)),
            DummyPlayer(name="D",
                        favorite_mode=(WENZ, None))]


@pytest.fixture
def game_state_during_bidding(player_hands_partner):
    leading_player = 0
    current_player = 3
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, BELLS), (NO_GAME, None)]
    game_mode = (PARTNER_MODE, BELLS)
    declaring_player = 1
    tricks = []
    current_trick = None
    possible_actions = [(NO_GAME, None), (WENZ, None)] + [(SOLO, suit) for suit in SUITS]
    return {"player_hands": player_hands_partner,
            "leading_player_index": leading_player,
            "current_player_index": current_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "declaring_player": declaring_player,
            "tricks": tricks,
            "current_trick": current_trick,
            "possible_actions": possible_actions}


@pytest.fixture
def game_state_after_bidding(player_hands_partner):
    leading_player = 0
    current_player = 3
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, BELLS), (NO_GAME, None), (WENZ, None), (NO_GAME, None)]
    game_mode = (WENZ, None)
    declaring_player = 3
    tricks = []
    current_trick = None
    possible_actions = [(OBER, ACORNS), (OBER, BELLS), (UNTER, BELLS), (ACE, BELLS),
                        (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)]
    return {"player_hands": player_hands_partner,
            "leading_player_index": leading_player,
            "current_player_index": current_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "declaring_player": declaring_player,
            "tricks": tricks,
            "current_trick": current_trick,
            "possible_actions": possible_actions}


@pytest.fixture
def game_before(game_state_partner, dummy_player_list):
    for player, hand in zip(dummy_player_list, game_state_partner["player_hands"]):
        player.pick_up_cards(hand)
    return BiddingGame(game_state=game_state_partner, playerlist=dummy_player_list)


@pytest.fixture
def game_during(game_state_during_bidding, dummy_player_list):
    for player, hand in zip(dummy_player_list, game_state_during_bidding["player_hands"]):
        player.pick_up_cards(hand)
    return BiddingGame(game_state=game_state_during_bidding, playerlist=dummy_player_list)


@pytest.fixture
def game_after(game_state_after_bidding, dummy_player_list):
    for player, hand in zip(dummy_player_list, game_state_after_bidding["player_hands"]):
        player.pick_up_cards(hand)
    return BiddingGame(game_state=game_state_after_bidding, playerlist=dummy_player_list)


def test_possible_partner_modes(game_before, player_hands_partner):
    assert game_before.determine_possible_partner_modes(player_hands_partner[0]) == {(PARTNER_MODE, ACORNS),
                                                                                    (PARTNER_MODE, LEAVES)}
    assert game_before.determine_possible_partner_modes(player_hands_partner[1]) == {(PARTNER_MODE, BELLS)}
    assert game_before.determine_possible_partner_modes(player_hands_partner[2]) == {(PARTNER_MODE, ACORNS),
                                                                                    (PARTNER_MODE, LEAVES),
                                                                                     (PARTNER_MODE, BELLS)}


def test_possible_game_modes(game_before, player_hands_partner):
    possible_modes = game_before.determine_possible_game_modes(player_hands_partner[0], mode_to_beat=NO_GAME)
    assert possible_modes == {(PARTNER_MODE, ACORNS), (PARTNER_MODE, LEAVES), (NO_GAME, None), (WENZ, None),
                              (SOLO, HEARTS), (SOLO, ACORNS), (SOLO, BELLS), (SOLO, LEAVES)}
    possible_modes = game_before.determine_possible_game_modes(player_hands_partner[1], mode_to_beat=NO_GAME)
    assert possible_modes == {(PARTNER_MODE, BELLS), (NO_GAME, None), (WENZ, None),
                              (SOLO, HEARTS), (SOLO, ACORNS), (SOLO, BELLS), (SOLO, LEAVES)}
    possible_modes = game_before.determine_possible_game_modes(player_hands_partner[0], mode_to_beat=WENZ)
    assert possible_modes == {(SOLO, HEARTS), (SOLO, ACORNS), (SOLO, BELLS), (SOLO, LEAVES), (NO_GAME, None)}


def test_bidding_game_init_before(game_before):
    assert game_before.current_player_index == 0
    assert game_before.deciding_players == {0, 1, 2, 3}
    assert game_before.mode_proposals == []
    assert not game_before.finished()


def test_bidding_game_init_during(game_during):
    assert game_during.current_player_index == 3
    assert game_during.deciding_players == {1, 3}
    assert not game_during.finished()
    assert game_during.game_mode == (PARTNER_MODE, BELLS)
    assert game_during.offensive_players == [1, 0]


def test_bidding_game_init_after(game_after):
    assert game_after.game_mode == (WENZ, None)
    assert game_after.deciding_players == {3}
    assert game_after.offensive_players == [3]
    assert game_after.finished()


def test_bidding_game_next_proposal(game_before):
    bidding_game = game_before
    assert bidding_game.mode_to_beat == 0
    assert bidding_game.deciding_players == {0, 1, 2, 3}
    assert bidding_game.current_player_index == 0
    bidding_game.next_proposal()
    assert bidding_game.game_mode == (NO_GAME, None)
    assert bidding_game.mode_to_beat == NO_GAME
    assert bidding_game.current_player_index == 1
    assert bidding_game.deciding_players == {1, 2, 3}
    assert not bidding_game.finished()
    bidding_game.next_proposal()
    assert bidding_game.mode_to_beat == PARTNER_MODE
    assert bidding_game.deciding_players == {1, 2, 3}
    assert not bidding_game.finished()
    bidding_game.next_proposal()
    assert bidding_game.deciding_players == {1, 3}
    assert bidding_game.current_player_index == 3
    assert not bidding_game.finished()
    bidding_game.next_proposal()
    assert bidding_game.mode_to_beat == PARTNER_MODE
    assert bidding_game.offensive_players == [3]
    assert not bidding_game.finished()
    bidding_game.next_proposal()
    assert bidding_game.game_mode == (WENZ, None)
    assert bidding_game.finished()
