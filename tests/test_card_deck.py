from schafkopf.card_deck import CardDeck
from schafkopf.suits import ACORNS, BELLS, HEARTS, LEAVES
from schafkopf.ranks import ACE, TEN, EIGHT, SEVEN
import pytest


@pytest.fixture
def card_deck():
    return CardDeck()


def test_deal_hand(card_deck):
    hand = card_deck.deal_hand()
    assert len(hand) == 8
    assert len(card_deck.cards) == 24
    assert hand == [(ACE, ACORNS), (ACE, LEAVES), (ACE, HEARTS), (ACE, BELLS),
                    (TEN, ACORNS), (TEN, LEAVES), (TEN, HEARTS), (TEN, BELLS)]


def test_deal_hands(card_deck):
    player_hands = card_deck.deal_player_hands()
    assert len(player_hands) == 4
    assert len(player_hands[2]) == 8
    assert len(card_deck.cards) == 0
    assert player_hands[3] == [(EIGHT, ACORNS), (EIGHT, LEAVES), (EIGHT, HEARTS), (EIGHT, BELLS),
                               (SEVEN, ACORNS), (SEVEN, LEAVES), (SEVEN, HEARTS), (SEVEN, BELLS)]
