import numpy as np
import schafkopf.players.data.load_data as ld
import schafkopf.players.data.encodings as enc
from schafkopf.game_modes import PARTNER_MODE
from schafkopf.ranks import KING
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


def test_prepare_data_inference():
    card_sequences, hands_to_predict = ld.prepare_data_inference(game_data_dic, num_samples=26)
    assert len(card_sequences) == 26
    assert len(hands_to_predict) == 26
    seq = card_sequences[0]
    hands = hands_to_predict[0]
    assert hands.shape == (128, )
    assert seq.shape == (28, 36)
    shortest_seq = None
    pl_hands = None
    for s, i in zip(card_sequences, range(len(hands_to_predict))):
        if np.array_equal(s[2][:32], np.zeros(32)):
            shortest_seq = s
            pl_hands = hands_to_predict[i]
    played_card = shortest_seq[1][:32]
    assert pl_hands.shape == (128, )
    assert enc.decode_one_hot_card(played_card) == (KING, LEAVES)
    goal = np.zeros(128)
    indices = [16, 29, 25, 21, 9, 23, 24, 46, 45, 33, 63, 59, 42, 34, 60, 83,
               82, 81, 76, 69, 75, 67, 90, 111, 103, 126, 102, 116, 104, 100, 96]
    for index in indices:
        goal[index] = 1
    for i in range(128):
        assert goal[i] == pl_hands[i], 'failed at card {}'.format(i)
    assert np.array_equal(goal, pl_hands)
