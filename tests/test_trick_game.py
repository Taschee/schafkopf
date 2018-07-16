import pytest
from schafkopf.trick_game import TrickGame
from schafkopf.players import DummyPlayer
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.suits import ACORNS, BELLS, HEARTS, LEAVES
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.trick import Trick


@pytest.fixture
def dummy_player_list():
    return [DummyPlayer(name="A", favorite_cards=[(OBER, ACORNS), (SEVEN, ACORNS), (ACE, BELLS), (OBER, BELLS),
                                                  (UNTER, BELLS), (KING, LEAVES), (TEN, ACORNS), (NINE, ACORNS)]),
            DummyPlayer(name="B", favorite_cards=[(ACE, HEARTS), (ACE, ACORNS), (KING, BELLS), (OBER, HEARTS),
                                                  (SEVEN, HEARTS), (OBER, LEAVES), (UNTER, ACORNS), (SEVEN, BELLS)]),
            DummyPlayer(name="C", favorite_cards=[(KING, HEARTS), (EIGHT, ACORNS), (NINE, BELLS), (TEN, HEARTS),
                                                  (UNTER, LEAVES), (TEN, LEAVES), (SEVEN, LEAVES), (KING, ACORNS)]),
            DummyPlayer(name="D", favorite_cards=[(EIGHT, HEARTS), (NINE, HEARTS), (EIGHT, BELLS), (UNTER, HEARTS),
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
def player_hands_during():
    return [[(OBER, BELLS), (ACE, BELLS),
             (KING, LEAVES), (TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)],
            [(OBER, HEARTS), (UNTER, ACORNS),
             (SEVEN, HEARTS), (KING, BELLS), (SEVEN, BELLS)],
            [(TEN, LEAVES), (KING, ACORNS),
             (TEN, HEARTS), (SEVEN, LEAVES), (NINE, BELLS)],
            [(UNTER, HEARTS), (ACE, LEAVES), (TEN, BELLS),
             (EIGHT, LEAVES), (EIGHT, BELLS), (NINE, LEAVES)]]


@pytest.fixture
def game_state_before_play(player_hands_before):
    leading_player = 0
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, BELLS), (NO_GAME, None), (NO_GAME, None)]
    game_mode = (PARTNER_MODE, BELLS)
    offensive_players = [1, 0]
    tricks = []
    current_trick = None
    return {"player_hands": player_hands_before,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": tricks,
            "current_trick": current_trick}


@pytest.fixture
def prev_tricks():
    first_trick = Trick(leading_player_index=0,
                        cards=[(OBER, ACORNS), (ACE, HEARTS), (KING, HEARTS), (EIGHT, HEARTS)],
                        winner=0,
                        score=18)
    sec_trick = Trick(leading_player_index=0,
                      cards=[(UNTER, BELLS), (OBER, LEAVES), (UNTER, LEAVES), (NINE, HEARTS)],
                      winner=1,
                      score=7)
    return [first_trick, sec_trick]


@pytest.fixture
def current_trick():
    curr_trick = Trick(leading_player_index=1,
                       cards=[None, (ACE, ACORNS), (EIGHT, ACORNS), None])
    return curr_trick


@pytest.fixture
def game_state_during_play(player_hands_during, prev_tricks, current_trick):
    leading_player = 0
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, BELLS), (NO_GAME, None), (NO_GAME, None)]
    game_mode = (PARTNER_MODE, BELLS)
    offensive_players = [1, 0]
    return {"player_hands": player_hands_during,
            "leading_player_index": leading_player,
            "mode_proposals": mode_proposals,
            "game_mode": game_mode,
            "offensive_players": offensive_players,
            "tricks": prev_tricks,
            "current_trick": current_trick}


@pytest.fixture
def trick_game_before(dummy_player_list, game_state_before_play):
    for player, hand in zip(dummy_player_list, game_state_before_play["player_hands"]):
        player.pick_up_cards(hand)
    return TrickGame(game_state=game_state_before_play, playerlist=dummy_player_list)


@pytest.fixture
def trick_game_during(dummy_player_list, game_state_during_play):
    for player, hand in zip(dummy_player_list, game_state_during_play["player_hands"]):
        player.pick_up_cards(hand)
    return TrickGame(game_state=game_state_during_play, playerlist=dummy_player_list)


def test_trick_game_init_before(trick_game_before):
    assert trick_game_before.current_player_index == 0
    assert len(trick_game_before.tricks) == 0
    assert trick_game_before.current_trick.num_cards == 0
    assert trick_game_before.game_mode == (PARTNER_MODE, BELLS)
    assert trick_game_before.offensive_players == [1, 0]
    assert trick_game_before.trumpcards == [(OBER, ACORNS), (OBER, LEAVES), (OBER, HEARTS), (OBER, BELLS),
                                     (UNTER, ACORNS), (UNTER, LEAVES), (UNTER, HEARTS), (UNTER, BELLS),
                                     (ACE, HEARTS), (TEN, HEARTS), (KING, HEARTS),
                                     (NINE, HEARTS), (EIGHT, HEARTS), (SEVEN, HEARTS)]
    assert not trick_game_before.finished()


def test_trick_game_init_during(trick_game_during, prev_tricks, current_trick):
    assert trick_game_during.current_player_index == 3
    assert len(trick_game_during.tricks) == 2
    assert trick_game_during.current_trick.num_cards == 2
    assert trick_game_during.game_mode == (PARTNER_MODE, BELLS)
    assert trick_game_during.offensive_players == [1, 0]
    assert trick_game_during.trumpcards == [(OBER, ACORNS), (OBER, LEAVES), (OBER, HEARTS), (OBER, BELLS),
                                            (UNTER, ACORNS), (UNTER, LEAVES), (UNTER, HEARTS), (UNTER, BELLS),
                                            (ACE, HEARTS), (TEN, HEARTS), (KING, HEARTS),
                                            (NINE, HEARTS), (EIGHT, HEARTS), (SEVEN, HEARTS)]
    assert trick_game_during.get_public_info() == {"leading_player_index": 0,
                                                   "mode_proposals": [(NO_GAME, None), (PARTNER_MODE, BELLS),
                                                                      (NO_GAME, None), (NO_GAME, None)],
                                                   "declaring_player": 1,
                                                   "game_mode": (PARTNER_MODE, BELLS),
                                                   "trumpcards": [(OBER, ACORNS), (OBER, LEAVES), (OBER, HEARTS),
                                                                  (OBER, BELLS), (UNTER, ACORNS), (UNTER, LEAVES),
                                                                  (UNTER, HEARTS), (UNTER, BELLS),
                                                                  (ACE, HEARTS), (TEN, HEARTS), (KING, HEARTS),
                                                                  (NINE, HEARTS), (EIGHT, HEARTS), (SEVEN, HEARTS)],
                                                   "tricks": prev_tricks,
                                                   "current_trick": current_trick}
    assert not trick_game_during.finished()


def test_suit_in_hand(trick_game_before):
    hand_0 = trick_game_before.playerlist[0].get_hand()
    assert trick_game_before.suit_in_hand(suit=BELLS, hand=hand_0) == [(ACE, BELLS)]
    assert trick_game_before.suit_in_hand(suit=ACORNS, hand=hand_0) == [(TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)]
    hand_1 = trick_game_before.playerlist[1].get_hand()
    assert trick_game_before.suit_in_hand(suit=LEAVES, hand=hand_1) == [(OBER, LEAVES), (OBER, HEARTS), (UNTER, ACORNS),
                                                                        (ACE, HEARTS), (SEVEN, HEARTS), (ACE, ACORNS),
                                                                        (KING, BELLS), (SEVEN, BELLS)]


def test_possible_cards(trick_game_during):
    curr_trick = trick_game_during.current_trick
    hand = trick_game_during.playerlist[3].get_hand()
    assert trick_game_during.possible_cards(current_trick=curr_trick,
                                            hand=hand) == [(UNTER, HEARTS), (ACE, LEAVES), (TEN, BELLS),
                                                           (EIGHT, LEAVES), (EIGHT, BELLS), (NINE, LEAVES)]
    hand = trick_game_during.playerlist[0].get_hand()
    assert trick_game_during.possible_cards(current_trick=curr_trick,
                                            hand=hand) == [(TEN, ACORNS), (SEVEN, ACORNS), (NINE, ACORNS)]
    curr_trick = Trick(leading_player_index=0,
                          cards=[(SEVEN, HEARTS), None, None, None])
    hand = trick_game_during.playerlist[3].get_hand()
    assert trick_game_during.possible_cards(current_trick=curr_trick,
                                            hand=hand) == [(UNTER, HEARTS)]
    hand = trick_game_during.playerlist[1].get_hand()
    assert trick_game_during.possible_cards(current_trick=curr_trick,
                                            hand=hand) == [(OBER, HEARTS), (UNTER, ACORNS), (SEVEN, HEARTS)]


def test_next_card(trick_game_before):
    game = trick_game_before
    assert game.current_trick.num_cards == 0
    game.play_next_card()
    assert game.current_trick.num_cards == 1
    assert game.current_trick.cards[0] == (OBER, ACORNS)
    assert not game.current_trick.finished()
    assert game.current_player_index == 0
    game.trick_finished()
    assert game.current_player_index == 1
    game.play_next_card()
    game.trick_finished()
    assert game.current_trick.num_cards == 2
    assert game.current_trick.cards[1] == (ACE, HEARTS)
    game.play_next_card()
    game.trick_finished()
    game.play_next_card()
    assert game.current_trick.finished()
    assert len(game.tricks) == 0
    game.trick_finished()
    assert len(game.tricks) == 1
    assert game.scores == [18, 0, 0, 0]
    assert game.current_player_index == 0
    for i in range(4):
        game.play_next_card()
        game.trick_finished()
    assert game.scores == [18, 0, 0, 11]
    assert game.current_player_index == 3
    assert game.tricks[1].cards[3] == (NINE, HEARTS)
    assert game.current_trick.num_cards == 0


def test_play(trick_game_before):
    trick_game_before.play()
    assert trick_game_before.finished()
    assert trick_game_before.scores == [33, 58, 4, 25]
    assert [trick.winner for trick in trick_game_before.tricks] == [0, 3, 0, 1, 2, 1, 1, 3]
