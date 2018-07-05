from schafkopf.game import Game, Trick
from schafkopf.players import RandomPlayer
import pytest

SIEBEN = 0
ACHT = 1
NEUN = 2
UNTER = 3
OBER = 4
KOENIG = 5
ZEHN = 6
AS = 7

SCHELLEN = 0
HERZ = 1
GRAS = 2
EICHEL = 3
SUITS = [EICHEL, GRAS, HERZ, SCHELLEN]

# every game mode is a tuple (game_type, suit). possible game_types are:
WEITER = 0
RUFSPIEL = 1
WENZ = 2
SOLO = 3

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
    hand1 = [(SIEBEN, SCHELLEN), (ACHT, SCHELLEN), (NEUN, HERZ), (SIEBEN, EICHEL),
             (KOENIG, EICHEL), (KOENIG, GRAS), (ZEHN, HERZ), (ZEHN, SCHELLEN)]
    hand2 = [(SIEBEN, HERZ), (OBER, SCHELLEN), (ACHT, HERZ), (NEUN, SCHELLEN),
             (KOENIG, HERZ), (UNTER, GRAS), (ZEHN, GRAS), (AS, EICHEL)]
    hand3 = [(NEUN, EICHEL), (UNTER, SCHELLEN), (UNTER, EICHEL), (OBER, EICHEL),
             (OBER, GRAS), (OBER, HERZ), (ZEHN, EICHEL), (AS, SCHELLEN)]
    hand4 = [(SIEBEN, GRAS), (ACHT, GRAS), (ACHT, EICHEL), (UNTER, HERZ),
             (NEUN, GRAS), (KOENIG, SCHELLEN), (AS, HERZ), (AS, GRAS)]
    player_hands = [hand1, hand2, hand3, hand4]
    leading_player_index = 0
    tricks = []
    current_trick = Trick(leading_player_index)
    mode_proposals = [(WEITER, None), (RUFSPIEL, GRAS)]
    game_state = (player_hands, leading_player_index, mode_proposals, tricks, current_trick)
    return game_state

@pytest.fixture
def example_game_state_trick_playing():
    hand1 = [(SIEBEN, SCHELLEN), (NEUN, HERZ), (SIEBEN, EICHEL),
             (KOENIG, EICHEL), (KOENIG, GRAS), (ZEHN, HERZ), (ZEHN, SCHELLEN)]
    hand2 = [(SIEBEN, HERZ), (OBER, SCHELLEN), (ACHT, HERZ),
             (KOENIG, HERZ), (UNTER, GRAS), (ZEHN, GRAS), (AS, EICHEL)]
    hand3 = [(NEUN, EICHEL), (UNTER, SCHELLEN), (UNTER, EICHEL),
             (OBER, GRAS), (OBER, HERZ), (ZEHN, EICHEL)]
    hand4 = [(SIEBEN, GRAS), (ACHT, GRAS), (UNTER, HERZ),
             (NEUN, GRAS), (AS, HERZ), (AS, GRAS)]
    player_hands = [hand1, hand2, hand3, hand4]
    leading_player_index = 0
    mode_proposals = [(WEITER, None), (RUFSPIEL, GRAS), (SOLO, EICHEL), (WEITER, None), (WEITER, None)]
    first_trick = Trick(leading_player_index=0)
    first_trick.cards = [(ACHT, SCHELLEN), (NEUN, SCHELLEN), (AS, SCHELLEN), (KOENIG, SCHELLEN)]
    first_trick.winner = 2
    first_trick.num_cards = 4
    first_trick.score = 15
    tricks = [first_trick]
    current_trick = Trick(leading_player_index=2)
    current_trick.cards[2] = (OBER, EICHEL)
    current_trick.cards[3] = (ACHT, EICHEL)
    current_trick.num_cards = 2
    current_trick.current_player = 0
    game_state = (player_hands, leading_player_index, mode_proposals, tricks, current_trick)
    return game_state

# testing the game mode decision part

def test_game_mode_initializing(game, example_game_state_mode_decision):
    mode_proposals = example_game_state_mode_decision[2]
    leading_player_index = example_game_state_mode_decision[1]
    game.initialize_game_mode(leading_player_index, mode_proposals)
    assert game.get_game_mode() == (RUFSPIEL, GRAS)
    assert not game.game_mode_decided()

def test_current_player(game, example_game_state_mode_decision):
    game.initialize_game_state(example_game_state_mode_decision)
    assert game.get_current_playerindex() == 2

def test_player_hands(game, example_game_state_mode_decision):
    game.initialize_game_state(example_game_state_mode_decision)
    player_hands =  example_game_state_mode_decision[0]
    players = game.get_players()
    assert player_hands[0] == players[0].get_hand()

# testing the trick playing part

def test_mode_initializing(game, example_game_state_trick_playing):
    mode_proposals = example_game_state_trick_playing[2]
    leading_player_index = example_game_state_trick_playing[1]
    game.initialize_game_mode(leading_player_index, mode_proposals)
    assert game.get_game_mode() == (SOLO, EICHEL)
    assert game.game_mode_decided()

def test_number_of_previous_tricks(game, example_game_state_trick_playing):
    game.initialize_game_state(example_game_state_trick_playing)
    assert len(game._tricks) == 1
