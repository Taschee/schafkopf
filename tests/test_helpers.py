import pytest
from schafkopf.game import Game, Trick
from schafkopf.players import RandomPlayer
import schafkopf.helpers as hlp

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


trumpcards = [(OBER, i) for i in SUITS] + [(UNTER, i) for i in SUITS] \
                                + [(AS, HERZ), (ZEHN, HERZ), (KOENIG, HERZ), (NEUN, HERZ), (ACHT, HERZ), (SIEBEN, HERZ)]

first_trick = Trick(leading_player_index=0)
first_trick.cards = [(NEUN, HERZ), (UNTER, EICHEL), (OBER, HERZ), (ZEHN, SCHELLEN)]
first_trick.score = 15
first_trick.winner = 2
sec_trick = Trick(leading_player_index=2)
sec_trick.cards = [(AS, GRAS), (AS, HERZ), (AS, EICHEL), (SIEBEN, EICHEL)]
sec_trick.score = 26
sec_trick.winner = 1

tricks = [first_trick, sec_trick]

current_trick = Trick(leading_player_index=1)
current_trick.cards = [None, (UNTER, SCHELLEN), (ZEHN, GRAS), None]

playerindex = 1
player_hand = [(ZEHN, HERZ), (OBER, GRAS), (UNTER, GRAS), (SIEBEN, GRAS), (OBER, SCHELLEN)]


def test_opp_cards_still_in_game():
    opp_cards = hlp.opponent_cards_still_in_game(tricks=tricks,
                                                 current_trick=current_trick,
                                                 player_hand=player_hand)
    assert set(opp_cards) == {(OBER, EICHEL), (UNTER, HERZ), (SIEBEN, HERZ), (ACHT, HERZ),
                              (KOENIG, HERZ), (ACHT, EICHEL), (NEUN, EICHEL), (ZEHN, EICHEL), (AS, SCHELLEN),
                              (KOENIG, SCHELLEN), (SIEBEN, SCHELLEN), (ACHT, SCHELLEN), (NEUN, SCHELLEN),
                              (KOENIG, GRAS), (KOENIG, EICHEL), (ACHT, GRAS), (NEUN, GRAS)}


def test_suit_not_followed():
    assert hlp.suits_not_followed(tricks, current_trick, trumpcards, playerindex=0) == [EICHEL]
    assert hlp.suits_not_followed(tricks, current_trick, trumpcards, playerindex=1) == [EICHEL]
    assert hlp.suits_not_followed(tricks, current_trick, trumpcards, playerindex=2) == []


def test_didnt_follow_trump():
    assert hlp.didnt_follow_trump(tricks, current_trick, trumpcards, playerindex=2)
    assert hlp.didnt_follow_trump(tricks, current_trick, trumpcards, playerindex=3)
    assert not hlp.didnt_follow_trump(tricks, current_trick, trumpcards, playerindex=1)


def test_distribution_possible():

    poss_hands = [[(OBER, EICHEL), (UNTER, HERZ), (SIEBEN, HERZ), (ACHT, HERZ), (KOENIG, HERZ), (ACHT, GRAS)],
                  player_hand,
                  [(SIEBEN, SCHELLEN), (ACHT, SCHELLEN), (NEUN, SCHELLEN), (KOENIG, GRAS), (KOENIG, EICHEL)],
                  [(ACHT, EICHEL), (NEUN, EICHEL), (ZEHN, EICHEL), (AS, SCHELLEN), (KOENIG, SCHELLEN), (NEUN, GRAS)]]

    assert hlp.card_distribution_possible(tricks=tricks, current_trick=current_trick, player_hands=poss_hands,
                                          playerindex=playerindex, trumpcards=trumpcards)

    not_poss_hands = [[(SIEBEN, SCHELLEN), (NEUN, EICHEL), (SIEBEN, HERZ), (ACHT, HERZ), (KOENIG, HERZ), (ACHT, GRAS)],
                      player_hand,
                      [(OBER, EICHEL), (ACHT, SCHELLEN), (NEUN, SCHELLEN), (KOENIG, GRAS), (KOENIG, EICHEL)],
                      [(ACHT, EICHEL), (UNTER, HERZ), (ZEHN, EICHEL), (AS, SCHELLEN), (KOENIG, SCHELLEN), (NEUN, GRAS)]]

    assert not hlp.card_distribution_possible(tricks=tricks, current_trick=current_trick,
                                              player_hands=not_poss_hands, playerindex=playerindex,
                                              trumpcards=trumpcards)

def test_sampling():
    player_hands = hlp.sample_opponent_hands(tricks=tricks, current_trick=current_trick, player_hand=player_hand,
                                             playerindex=playerindex, trumpcards=trumpcards)
    assert hlp.card_distribution_possible(tricks=tricks, current_trick=current_trick, trumpcards=trumpcards,
                                          playerindex=playerindex, player_hands=player_hands)
