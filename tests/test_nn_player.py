import numpy as np
from schafkopf.players.nn_player import NNPlayer
from schafkopf.players import DummyPlayer
from schafkopf.tournaments.game_states_trick_play import sample_game_states
from schafkopf.game import Game
from schafkopf.suits import *
from schafkopf.ranks import *
import pytest

@pytest.fixture
def example_public_info():
    game_state = sample_game_states[0]
    players = [DummyPlayer(favorite_cards=[(OBER, HEARTS), (TEN, BELLS)]),
               DummyPlayer(favorite_cards=[(OBER, ACORNS), (KING, BELLS)]),
               DummyPlayer(favorite_cards=[(SEVEN, HEARTS), (ACE, BELLS)]),
               DummyPlayer(favorite_cards=[(ACE, HEARTS), (EIGHT, BELLS)])]
    game = Game(players=players, game_state=game_state)
    for _ in range(8):
        game.next_action()
    return game.get_public_info()


def test_create_card_sequence(example_public_info):
    seq = NNPlayer().create_card_sequence(public_info=example_public_info)
    first_card, first_pl = seq[0]
    third_card, third_pl = seq[2]
    last_card, last_pl = seq[7]
    assert len(seq) == 8
    assert first_card == (OBER, HEARTS)
    assert first_pl == 0
    assert third_card == (SEVEN, HEARTS)
    assert third_pl == 2
    assert last_card == (TEN, BELLS)
    assert last_pl == 0


def test_switch_suits_card_sequence(example_public_info):
    pl = NNPlayer()
    seq = pl.create_card_sequence(public_info=example_public_info)
    switched_seq = pl.switch_suits(seq, example_public_info)
    fifth_card, fifth_pl = switched_seq[4]
    sec_card, sec_pl = switched_seq[1]
    assert fifth_card == (KING, ACORNS)
    assert fifth_pl == 1
    assert sec_card == (OBER, ACORNS)
    assert sec_pl == 1


def test_prediction(example_public_info):
    player = NNPlayer(game_mode_nn='../schafkopf/players/models/bigger_classifier_sortedhands_lr0.02.hdf5',
                      partner_nn='../schafkopf/players/models/partner_model_bigger_1.hdf5',
                      solo_nn='../schafkopf/players/models/solo_model_bigger_1.hdf5',
                      wenz_nn='../schafkopf/players/models/wenz_model_bigger_1.hdf5')
    prediction = player.make_card_prediction(example_public_info)
    print('\n Prediction : \n',player.make_card_prediction(example_public_info))
    assert len(prediction) == 32


def test_suits_options(example_public_info):
    pl = NNPlayer()
    options = [(3, 1), (3, 3), (6, 2), (6, 1), (3, 0), (0, 2)]
    assert pl.switch_suits_options(options, example_public_info) == [(3, 1), (3, 3), (6, 2), (6, 1), (3, 0), (0, 2)]
    other_options = [(2, 0), (3, 3), (5, 3), (1, 1), (0, 0)]
    assert pl.switch_suits_options(other_options, example_public_info) == [(2, 3), (3, 3), (5, 0), (1, 1), (0, 3)]

