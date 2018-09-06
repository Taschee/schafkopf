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
    assert enc.encode_one_hot_card(card).all() == encoded.all()
    assert enc.encode_one_hot_card(card2).all() == encoded2.all()
    assert enc.encode_one_hot_card(card3).all() == encoded3.all()
    assert enc.encode_one_hot_card(card4).all() == encoded4.all()
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
    assert enc.encode_one_hot_game_mode((PARTNER_MODE, LEAVES)).all() == partner_leaves_encoded.all()
    for mode in possible_modes:
        assert enc.decode_one_hot_game_mode(enc.encode_one_hot_game_mode(mode)) == mode


def test_one_hot_player_position():
    enc_pos = np.zeros(8)
    enc_pos[2] = 1
    assert enc.encode_one_hot_player_position(2).all() == enc_pos.all()
    for pos in range(4):
        assert enc.decode_one_hot_player_position(enc.encode_one_hot_player_position(pos)) == pos
