import schafkopf.players.data.encodings as enc
from schafkopf.game_modes import SOLO, WENZ, PARTNER_MODE, NO_GAME
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE, RANKS
from schafkopf.suits import HEARTS, LEAVES, ACORNS, BELLS, SUITS
import numpy as np


def test_one_hot_card_encoding():
    card = (SEVEN, HEARTS)
    encoded = np.zeros(32)
    encoded[1] = 1
    card2 = (OBER, ACORNS)
    encoded2 = np.zeros(32)
    encoded2[19] = 1
    card3 = (ACE, BELLS)
    encoded3 = np.zeros(32)
    encoded3[28] = 1
    card4 = (NINE, LEAVES)
    encoded4 = np.zeros(32)
    encoded4[10] = 1
    assert np.array_equal(enc.encode_one_hot_card(card), encoded)
    assert np.array_equal(enc.encode_one_hot_card(card2), encoded2)
    assert np.array_equal(enc.encode_one_hot_card(card3), encoded3)
    assert np.array_equal(enc.encode_one_hot_card(card4), encoded4)
    for suit in SUITS:
        for rank in RANKS:
            card = (rank, suit)
            assert enc.decode_one_hot_card(enc.encode_one_hot_card(card)) == card


def test_one_hot_game_mode_encoding():
    possible_modes = [(NO_GAME, None), (WENZ, None)] \
                      + [(PARTNER_MODE, suit) for suit in {ACORNS, BELLS, LEAVES}]\
                      + [(SOLO, suit) for suit in SUITS]
    partner_leaves_encoded = np.zeros(9)
    partner_leaves_encoded[2] = 1
    assert np.array_equal(enc.encode_one_hot_game_mode((PARTNER_MODE, LEAVES)), partner_leaves_encoded)
    for mode in possible_modes:
        assert enc.decode_one_hot_game_mode(enc.encode_one_hot_game_mode(mode)) == mode


def test_one_hot_player_position():
    enc_pos = np.zeros(4)
    enc_pos[2] = 1
    assert np.array_equal(enc.encode_one_hot_player_position(2), enc_pos)
    for pos in range(4):
        assert enc.decode_one_hot_player_position(enc.encode_one_hot_player_position(pos)) == pos


def test_one_hot_encoding_hand():
    hand = [(NINE, HEARTS), (SEVEN, ACORNS), (OBER, BELLS), (UNTER, HEARTS),
            (EIGHT, LEAVES), (TEN, LEAVES), (ACE, HEARTS), (KING, BELLS)]
    first_card_enc = np.zeros(32)
    first_card_enc[16] = 1
    assert np.array_equal(enc.encode_one_hot_hand(hand)[0], first_card_enc)
    sec_card_enc = np.zeros(32)
    sec_card_enc[13] = 1
    assert np.array_equal(enc.encode_one_hot_hand(hand)[1], sec_card_enc)


def test_encode_played_cards():
    seq = [((OBER, ACORNS), 1), ((UNTER, BELLS), 2), ((TEN, ACORNS), 3), ((EIGHT, HEARTS), 0), ((NINE, HEARTS), 1)]
    next_rel_pos = 2
    goal = np.zeros((28, 36))
    goal[0][33] = 1
    goal[1][34] = 1
    goal[1][19] = 1
    goal[2][35] = 1
    goal[2][12] = 1
    goal[3][32] = 1
    goal[3][27] = 1
    goal[4][33] = 1
    goal[4][5] = 1
    goal[5][34] = 1
    goal[5][9] = 1
    assert np.array_equal(enc.encode_played_cards(seq, next_rel_pos), goal)
    seq = []
    next_rel_pos = 3
    goal = np.zeros((28, 36))
    goal[0][35] = 1
    assert np.array_equal(enc.encode_played_cards(seq, next_rel_pos), goal)
