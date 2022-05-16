from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS, SUITS
from schafkopf.ranks import RANKS, SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.helpers import sort_hand


class Player:
    def __init__(self, name="Rando Calrissian"):
        self.name = name
        self.hand = []
        self.starting_hand = []
        return

    def pick_up_cards(self, hand, trumpcards=None):
        self.hand = sort_hand(hand, trumpcards)

    def set_starting_hand(self, hand, previous_tricks=None, playerindex=None, trumpcards=None):
        starting_hand = hand[:]
        if previous_tricks is not None:
            for trick in previous_tricks:
                card = trick.cards[playerindex]
                if card is not None:
                    starting_hand += [card]
        if trumpcards is None:
            self.starting_hand = sort_hand(starting_hand,
                                           trumpcards=[(OBER, ACORNS), (OBER, LEAVES), (OBER, HEARTS),
                                                       (OBER, BELLS), (UNTER, ACORNS), (UNTER, LEAVES),
                                                       (UNTER, HEARTS), (UNTER, BELLS), (ACE, HEARTS),
                                                       (TEN, HEARTS), (KING, HEARTS), (NINE, HEARTS),
                                                       (EIGHT, HEARTS), (SEVEN, HEARTS)])
        else:
            self.starting_hand = sort_hand(starting_hand, trumpcards=trumpcards)

    def number_of_cards(self):
        return len(self.hand)

    def get_hand(self):
        return self.hand

    def get_starting_hand(self):
        return self.starting_hand

    def get_player_position(self, game_state):
        for pos in range(4):
            hand = set(game_state['player_hands'][pos])
            if len(hand & set(self.starting_hand)) > 0:
                return pos
