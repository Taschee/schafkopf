from schafkopf.suits import SUITS
from schafkopf.ranks import RANKS
import random


class CardDeck:
    def __init__(self):
        self.cards = []
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append((rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards

    def deal_hand(self):
        hand = self.cards[:8]
        self.cards = self.cards[8:]
        return hand

    def deal_player_hands(self):
        player_hands = []
        for player in range(4):
            hand = self.deal_hand()
            player_hands.append(hand)
        return player_hands
