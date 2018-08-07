from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS, SUITS
from schafkopf.ranks import RANKS

class Player:
    def __init__(self, name="Rando Calrissian"):
        self._name = name
        self._hand = []
        self._starting_hand = []
        return

    def pick_up_cards(self, hand):
        self._hand = hand
        self._starting_hand = hand[:]

    def number_of_cards(self):
        return len(self._hand)

    def get_hand(self):
        return self._hand

    def get_starting_hand(self):
        return self._starting_hand

    def sort_hand(self, trumpcards):
        trumps_in_hand = [trump for trump in trumpcards if trump in self._hand]
        bells = [(i, BELLS) for i in RANKS if (i, BELLS) in self._hand and (i, BELLS) not in trumpcards]
        hearts = [(i, HEARTS) for i in RANKS if (i, HEARTS) in self._hand and (i, HEARTS) not in trumpcards]
        leaves = [(i, LEAVES) for i in RANKS if (i, LEAVES) in self._hand and (i, LEAVES) not in trumpcards]
        acorns = [(i, ACORNS) for i in RANKS if (i, ACORNS) in self._hand and (i, ACORNS) not in trumpcards]
        sorted_hand = trumps_in_hand + acorns + leaves + hearts + bells
        self._hand = sorted_hand