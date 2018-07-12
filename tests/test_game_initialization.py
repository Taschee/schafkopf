from schafkopf.game import Game, Trick
from schafkopf.players import RandomPlayer
from schafkopf.suits import BELLS, HEARTS, LEAVES, ACORNS, SUITS
from schafkopf.ranks import SEVEN, EIGHT, NINE, UNTER, OBER, KING, TEN, ACE, RANKS
from  schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
import pytest


@pytest.fixture
def game():
    '''Returns a new Schafkopf game with Random Players'''
    player1 = RandomPlayer()
    player2 = RandomPlayer()
    player3 = RandomPlayer()
    player4 = RandomPlayer()
    randomplayer_list = [player1, player2, player3, player4]
    return Game(randomplayer_list)


@pytest.fixture
def example_game_state_mode_decision():
    hand1 = [(SEVEN, BELLS), (EIGHT, BELLS), (NINE, HEARTS), (SEVEN, ACORNS),
             (KING, ACORNS), (KING, LEAVES), (TEN, HEARTS), (TEN, BELLS)]
    hand2 = [(SEVEN, HEARTS), (OBER, BELLS), (EIGHT, HEARTS), (NINE, BELLS),
             (KING, HEARTS), (UNTER, LEAVES), (TEN, LEAVES), (ACE, ACORNS)]
    hand3 = [(NINE, ACORNS), (UNTER, BELLS), (UNTER, ACORNS), (OBER, ACORNS),
             (OBER, LEAVES), (OBER, HEARTS), (TEN, ACORNS), (ACE, BELLS)]
    hand4 = [(SEVEN, LEAVES), (EIGHT, LEAVES), (EIGHT, ACORNS), (UNTER, HEARTS),
             (NINE, LEAVES), (KING, BELLS), (ACE, HEARTS), (ACE, LEAVES)]
    player_hands = [hand1, hand2, hand3, hand4]
    leading_player_index = 0
    tricks = []
    current_trick = Trick(leading_player_index)
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, LEAVES)]
    game_state = {"player_hands": player_hands,
                  "leading_player_index": leading_player_index,
                  "mode_proposals": mode_proposals,
                  "tricks": tricks,
                  "current_trick": current_trick}
    return game_state


@pytest.fixture
def example_game_state_trick_playing():
    hand1 = [(SEVEN, BELLS), (NINE, HEARTS), (SEVEN, ACORNS),
             (KING, ACORNS), (KING, LEAVES), (TEN, HEARTS), (TEN, BELLS)]
    hand2 = [(SEVEN, HEARTS), (OBER, BELLS), (EIGHT, HEARTS),
             (KING, HEARTS), (UNTER, LEAVES), (TEN, LEAVES), (ACE, ACORNS)]
    hand3 = [(NINE, ACORNS), (UNTER, BELLS), (UNTER, ACORNS),
             (OBER, LEAVES), (OBER, HEARTS), (TEN, ACORNS)]
    hand4 = [(SEVEN, LEAVES), (EIGHT, LEAVES), (UNTER, HEARTS),
             (NINE, LEAVES), (ACE, HEARTS), (ACE, LEAVES)]
    player_hands = [hand1, hand2, hand3, hand4]
    leading_player_index = 0
    mode_proposals = [(NO_GAME, None), (PARTNER_MODE, LEAVES), (SOLO, ACORNS), (NO_GAME, None), (NO_GAME, None)]
    first_trick = Trick(leading_player_index=0)
    first_trick.cards = [(EIGHT, BELLS), (NINE, BELLS), (ACE, BELLS), (KING, BELLS)]
    first_trick.winner = 2
    first_trick.num_cards = 4
    first_trick.score = 15
    tricks = [first_trick]
    current_trick = Trick(leading_player_index=2)
    current_trick.cards[2] = (OBER, ACORNS)
    current_trick.cards[3] = (EIGHT, ACORNS)
    current_trick.num_cards = 2
    current_trick.current_player = 0
    game_state = {"player_hands": player_hands,
                  "leading_player_index": leading_player_index,
                  "mode_proposals": mode_proposals,
                  "tricks": tricks,
                  "current_trick": current_trick}
    return game_state


# testing the game mode decision part


def test_initialize_game_mode(game, example_game_state_mode_decision):
    mode_proposals = example_game_state_mode_decision["mode_proposals"]
    leading_player_index = example_game_state_mode_decision["leading_player_index"]
    game.initialize_game_mode(leading_player_index, mode_proposals)
    assert game.get_game_mode() == (PARTNER_MODE, LEAVES)
    assert not game.game_mode_decided()


def test_current_player(game, example_game_state_mode_decision):
    game.initialize_game_state(example_game_state_mode_decision)
    assert game.get_current_playerindex() == 2


def test_player_hands(game, example_game_state_mode_decision):
    game.initialize_game_state(example_game_state_mode_decision)
    player_hands =  example_game_state_mode_decision["player_hands"]
    players = game.get_players()
    for player, hand in zip(players, player_hands):
        assert hand == player.get_hand()


# testing the trick playing part


def test_mode_initializing(game, example_game_state_trick_playing):
    mode_proposals = example_game_state_trick_playing["mode_proposals"]
    leading_player_index = example_game_state_trick_playing["leading_player_index"]
    game.initialize_game_mode(leading_player_index, mode_proposals)
    assert game.get_game_mode() == (SOLO, ACORNS)
    assert game.game_mode_decided()


def test_previous_tricks(game, example_game_state_trick_playing):
    game.initialize_game_state(example_game_state_trick_playing)
    assert len(game.get_tricks()) == 1
    assert game.get_tricks()[0].score == 15


def test_current_trick(game, example_game_state_trick_playing):
    game.initialize_game_state(example_game_state_trick_playing)
    curr_trick = game.get_current_trick()
    assert curr_trick.num_cards == 2
    assert curr_trick.current_player == 0
    assert curr_trick.cards[2] == (OBER, ACORNS)
