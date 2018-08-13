from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS, SUITS
from schafkopf.ranks import RANKS

class Player:
    def __init__(self, name="Rando Calrissian"):
        self.name = name
        self.hand = []
        self.starting_hand = []
        return

    def pick_up_cards(self, hand):
        self.hand = hand
        self.starting_hand = hand[:]

    def number_of_cards(self):
        return len(self.hand)

    def get_hand(self):
        return self.hand

    def get_starting_hand(self):
        return self.starting_hand

    def sort_hand(self, trumpcards):
        trumps_in_hand = [trump for trump in trumpcards if trump in self.hand]
        bells = [(i, BELLS) for i in RANKS if (i, BELLS) in self.hand and (i, BELLS) not in trumpcards]
        hearts = [(i, HEARTS) for i in RANKS if (i, HEARTS) in self.hand and (i, HEARTS) not in trumpcards]
        leaves = [(i, LEAVES) for i in RANKS if (i, LEAVES) in self.hand and (i, LEAVES) not in trumpcards]
        acorns = [(i, ACORNS) for i in RANKS if (i, ACORNS) in self.hand and (i, ACORNS) not in trumpcards]
        sorted_hand = trumps_in_hand + acorns + leaves + hearts + bells
        self.hand = sorted_hand