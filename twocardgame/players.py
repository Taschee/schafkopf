
import random


class Player:
    def __init__(self, name="Rando Calrissian"):
        self._name = name
        self._hand = []
        return

    def pick_up_cards(self, hand):
        self._hand = hand
        self.sort_hand()

    def number_of_cards(self):
        return len(self._hand)

    def get_hand(self):
        return self._hand

    def sort_hand(self):
        trumps_in_hand = [trump for trump in [(3,0), (2,0), (1,0)] if trump in self._hand]
        schellen = [(i, 1) for i in range(3, -1, -1) if (i, 1) in self._hand]
        sorted_hand = trumps_in_hand + schellen
        self._hand = sorted_hand

class RandomPlayer(Player):

    def choose_game_mode(self, options):
        return random.choice(tuple(options))

    def play_card(self, previous_cards, options=None, card=None):
        if options is None:
            card = random.choice(self._hand)
        else:
            card = random.choice(options)
        self._hand.remove(card)
        return card

class CFRPlayer(Player):

    def choose_game_mode(self, options):
        return 0

    def play_card(self, previous_cards, options=None, card=None):
        if card is not None:
            if card not in options:
                print("Card not legal")
            else:
                self._hand.remove(card)
                return card
        if card is None:
            if options is None:
                return random.choice(self._hand)
            else:
                return random.choice(options)


