import numpy as np
import schafkopf.players.data.load_data as ld


filepath = 'test_data.p'


def test_num_games_in_file():
    assert ld.num_games_in_file(filepath) == 2751


def test_num_augmented_examples_in_file():
    assert ld.num_augmented_examples_in_file(filepath) == 113040
