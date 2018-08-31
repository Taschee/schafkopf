from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS, SUITS
from schafkopf.ranks import RANKS, SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE

class Player:
    def __init__(self, name="Rando Calrissian"):
        self.name = name
        self.hand = []
        self.starting_hand = []
        return

    def pick_up_cards(self, hand, trumpcards=None):
        if trumpcards is None:
            self.hand = self.sort_hand(hand=hand, trumpcards=[(OBER, ACORNS), (OBER, LEAVES), (OBER, HEARTS),
                                                              (OBER, BELLS), (UNTER, ACORNS), (UNTER, LEAVES),
                                                              (UNTER, HEARTS), (UNTER, BELLS), (ACE, HEARTS),
                                                              (TEN, HEARTS), (KING, HEARTS), (NINE, HEARTS),
                                                              (EIGHT, HEARTS), (SEVEN, HEARTS)])
        else:
            self.hand = self.sort_hand(hand, trumpcards)

    def set_starting_hand(self, hand, previous_tricks=None, playerindex=None, trumpcards=None):
        starting_hand = hand[:]
        if previous_tricks is not None:
            for trick in previous_tricks:
                card = trick.cards[playerindex]
                if card is not None:
                    starting_hand += [card]
        if trumpcards is None:
            self.starting_hand = self.sort_hand(starting_hand,
                                                trumpcards=[(OBER, ACORNS), (OBER, LEAVES), (OBER, HEARTS),
                                                            (OBER, BELLS), (UNTER, ACORNS), (UNTER, LEAVES),
                                                            (UNTER, HEARTS), (UNTER, BELLS), (ACE, HEARTS),
                                                            (TEN, HEARTS), (KING, HEARTS), (NINE, HEARTS),
                                                            (EIGHT, HEARTS), (SEVEN, HEARTS)])
        else:
            self.starting_hand = self.sort_hand(starting_hand, trumpcards=trumpcards)

    def number_of_cards(self):
        return len(self.hand)

    def get_hand(self):
        return self.hand

    def get_starting_hand(self):
        return self.starting_hand

    def sort_hand(self, hand, trumpcards):
        trumps_in_hand = [trump for trump in trumpcards if trump in hand]
        bells = [(i, BELLS) for i in RANKS if (i, BELLS) in hand and (i, BELLS) not in trumpcards]
        hearts = [(i, HEARTS) for i in RANKS if (i, HEARTS) in hand and (i, HEARTS) not in trumpcards]
        leaves = [(i, LEAVES) for i in RANKS if (i, LEAVES) in hand and (i, LEAVES) not in trumpcards]
        acorns = [(i, ACORNS) for i in RANKS if (i, ACORNS) in hand and (i, ACORNS) not in trumpcards]
        sorted_hand = trumps_in_hand + acorns + leaves + hearts + bells
        return sorted_hand