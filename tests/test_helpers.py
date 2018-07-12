import pytest
from schafkopf.trick import Trick
import schafkopf.helpers as hlp
from schafkopf.suits import BELLS, HEARTS, LEAVES, ACORNS, SUITS
from schafkopf.ranks import SEVEN, EIGHT, NINE, UNTER, OBER, KING, TEN, ACE, RANKS


trumpcards = [(OBER, i) for i in SUITS] + [(UNTER, i) for i in SUITS] \
                    + [(ACE, HEARTS), (TEN, HEARTS), (KING, HEARTS), (NINE, HEARTS), (EIGHT, HEARTS), (SEVEN, HEARTS)]

first_trick = Trick(leading_player_index=0)
first_trick.cards = [(NINE, HEARTS), (UNTER, ACORNS), (OBER, HEARTS), (TEN, BELLS)]
first_trick.score = 15
first_trick.winner = 2
sec_trick = Trick(leading_player_index=2)
sec_trick.cards = [(ACE, LEAVES), (ACE, HEARTS), (ACE, ACORNS), (SEVEN, ACORNS)]
sec_trick.score = 26
sec_trick.winner = 1

tricks = [first_trick, sec_trick]

current_trick = Trick(leading_player_index=1)
current_trick.cards = [None, (UNTER, BELLS), (TEN, LEAVES), None]

playerindex = 1
player_hand = [(TEN, HEARTS), (OBER, LEAVES), (UNTER, LEAVES), (SEVEN, LEAVES), (OBER, BELLS)]


def test_opp_cards_still_in_game():
    opp_cards = hlp.opponent_cards_still_in_game(tricks=tricks,
                                                 current_trick=current_trick,
                                                 player_hand=player_hand)
    assert set(opp_cards) == {(OBER, ACORNS), (UNTER, HEARTS), (SEVEN, HEARTS), (EIGHT, HEARTS),
                              (KING, HEARTS), (EIGHT, ACORNS), (NINE, ACORNS), (TEN, ACORNS), (ACE, BELLS),
                              (KING, BELLS), (SEVEN, BELLS), (EIGHT, BELLS), (NINE, BELLS),
                              (KING, LEAVES), (KING, ACORNS), (EIGHT, LEAVES), (NINE, LEAVES)}


def test_suit_not_followed():
    assert hlp.suits_not_followed(tricks, current_trick, trumpcards, playerindex=0) == [ACORNS]
    assert hlp.suits_not_followed(tricks, current_trick, trumpcards, playerindex=1) == [ACORNS]
    assert hlp.suits_not_followed(tricks, current_trick, trumpcards, playerindex=2) == []


def test_didnt_follow_trump():
    assert hlp.didnt_follow_trump(tricks, current_trick, trumpcards, playerindex=2)
    assert hlp.didnt_follow_trump(tricks, current_trick, trumpcards, playerindex=3)
    assert not hlp.didnt_follow_trump(tricks, current_trick, trumpcards, playerindex=1)


def test_distribution_possible():

    poss_hands = [[(OBER, ACORNS), (UNTER, HEARTS), (SEVEN, HEARTS), (EIGHT, HEARTS), (KING, HEARTS), (EIGHT, LEAVES)],
                  player_hand,
                  [(SEVEN, BELLS), (EIGHT, BELLS), (NINE, BELLS), (KING, LEAVES), (KING, ACORNS)],
                  [(EIGHT, ACORNS), (NINE, ACORNS), (TEN, ACORNS), (ACE, BELLS), (KING, BELLS), (NINE, LEAVES)]]

    assert hlp.card_distribution_possible(tricks=tricks, current_trick=current_trick, player_hands=poss_hands,
                                          playerindex=playerindex, trumpcards=trumpcards)

    not_poss_hands = [[(SEVEN, BELLS), (NINE, ACORNS), (SEVEN, HEARTS), (EIGHT, HEARTS), (KING, HEARTS), (EIGHT, LEAVES)],
                      player_hand,
                      [(OBER, ACORNS), (EIGHT, BELLS), (NINE, BELLS), (KING, LEAVES), (KING, ACORNS)],
                      [(EIGHT, ACORNS), (UNTER, HEARTS), (TEN, ACORNS), (ACE, BELLS), (KING, BELLS), (NINE, LEAVES)]]

    assert not hlp.card_distribution_possible(tricks=tricks, current_trick=current_trick,
                                              player_hands=not_poss_hands, playerindex=playerindex,
                                              trumpcards=trumpcards)

def test_sampling():
    player_hands = hlp.sample_opponent_hands(tricks=tricks, current_trick=current_trick, player_hand=player_hand,
                                             playerindex=playerindex, trumpcards=trumpcards)
    assert hlp.card_distribution_possible(tricks=tricks, current_trick=current_trick, trumpcards=trumpcards,
                                          playerindex=playerindex, player_hands=player_hands)
