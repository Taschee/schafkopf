
import random

class Player:
    def __init__(self, name="Rando Calrissian"):
        self._name = name
        self._hand = []
        return

    def pick_up_cards(self, hand):
        self._hand = hand

    def number_of_cards(self):
        return len(self._hand)

    def get_hand(self):
        return self._hand

    def sort_hand(self, trumpcards):
        trumps_in_hand = [trump for trump in trumpcards if trump in self._hand]
        schellen = [(i, 0) for i in range(7, -1, -1) if (i, 0) in self._hand and (i, 0) not in trumpcards]
        herz = [(i, 1) for i in range(7, -1, -1) if (i, 1) in self._hand and (i, 1) not in trumpcards]
        gras = [(i, 2) for i in range(7, -1, -1) if (i, 2) in self._hand and (i, 2) not in trumpcards]
        eichel = [(i, 3) for i in range(7, -1, -1) if (i, 3) in self._hand and (i, 3) not in trumpcards]
        sorted_hand = trumps_in_hand + eichel + gras + herz + schellen
        self._hand = sorted_hand

class RandomPlayer(Player):

    def choose_game_mode(self, options):
        return random.choice(tuple(options))

    def play_card(self, previous_cards, options=None):
        if options is None:
            card = random.choice(self._hand)
        else:
            card = random.choice(options)
        self._hand.remove(card)
        return card


class HumanPlayer:
    def __init__(self, name):
        self._name = name
        self._hand = []
        return

    def pick_up_cards(self, hand):
        self._hand = hand

    def number_of_cards(self):
        return len(self._hand)

    def get_hand(self):
        return self._hand

    def choose_game_mode(self, options):
        # ToDo
        return

    def play_card(self, card, options=None):
        if card in self._hand:
            self._hand.remove(card)
        return card
