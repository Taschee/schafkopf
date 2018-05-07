
import random


class RandomPlayer:
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

    def play_card(self, options=None):
        # ToDo
        return
