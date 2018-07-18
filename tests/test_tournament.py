import pytest
from schafkopf.tournament import Tournament
from schafkopf.players import RandomPlayer


@pytest.fixture
def rand_tournament(random_player_list):
    return Tournament(playerlist=random_player_list, number_of_games=32)


def test_play_next_game(rand_tournament):
    assert rand_tournament.leading_player_index == 0
    rand_tournament.play_next_game()
    assert rand_tournament.leading_player_index == 1
    assert len(rand_tournament.games) == 1
    assert sum(rand_tournament.cumulative_rewards) == 0


def test_play(rand_tournament):
    rand_tournament.play()
    assert rand_tournament.finished()
    assert len(rand_tournament.games) == 32
    assert sum(rand_tournament.cumulative_rewards) == 0
