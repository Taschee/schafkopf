import numpy as np
import schafkopf.players.data.load_data as ld
from schafkopf.game_modes import PARTNER_MODE
from schafkopf.suits import BELLS, ACORNS, LEAVES, HEARTS


filepath = 'test_data.p'
game_data_dic = {'player_hands': [[(4, 0), (7, 1), (6, 1), (5, 1), (2, 1), (5, 3), (5, 2), (6, 0)],
                                  [(3, 2), (3, 1), (0, 1), (7, 3), (6, 3), (2, 2), (0, 2), (7, 0)],
                                  [(4, 3), (4, 2), (4, 1), (3, 0), (1, 1), (2, 3), (0, 3), (6, 2)],
                                  [(3, 3), (1, 3), (7, 2), (1, 2), (5, 0), (2, 0), (1, 0), (0, 0)]],
                 'game_mode': (PARTNER_MODE, LEAVES),
                 'played_cards': [((5, 2), 0), ((0, 2), 1), ((6, 2), 2), ((7, 2), 3), ((1, 2), 3), ((7, 1), 0),
                                  ((2, 2), 1), ((3, 0), 2), ((4, 3), 2), ((3, 3), 3), ((2, 1), 0), ((0, 1), 1),
                                  ((4, 2), 2), ((5, 0), 3), ((6, 1), 0), ((3, 1), 1), ((0, 3), 2), ((1, 3), 3),
                                  ((5, 3), 0), ((7, 3), 1), ((6, 3), 1), ((2, 3), 2), ((2, 0), 3), ((6, 0), 0),
                                  ((7, 0), 1), ((4, 1), 2), ((0, 0), 3), ((5, 1), 0), ((1, 1), 2), ((1, 0), 3),
                                  ((4, 0), 0), ((3, 2), 1)],
                 'declaring_player': 2}


def test_num_games_in_file():
    assert ld.num_games_in_file(filepath) == 2751


def test_num_augmented_examples_in_file():
    assert ld.num_augmented_games_in_file(filepath) == 28260


def test_prepare_data_bidding():
    data_list = ld.prepare_data_bidding(game_data_dic)
    assert len(data_list) == 4
    x, y = data_list[0]
    assert x.shape == (8, 32)
    assert y.shape == (9, )
    data_list_augmented = ld.prepare_data_bidding(game_data_dic, augment_data=True)
    assert len(data_list_augmented) == 24
