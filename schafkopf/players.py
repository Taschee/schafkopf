from schafkopf.game_modes import NO_GAME
import random

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
        schellen = [(i, 0) for i in range(7, -1, -1) if (i, 0) in self._hand and (i, 0) not in trumpcards]
        herz = [(i, 1) for i in range(7, -1, -1) if (i, 1) in self._hand and (i, 1) not in trumpcards]
        gras = [(i, 2) for i in range(7, -1, -1) if (i, 2) in self._hand and (i, 2) not in trumpcards]
        eichel = [(i, 3) for i in range(7, -1, -1) if (i, 3) in self._hand and (i, 3) not in trumpcards]
        sorted_hand = trumps_in_hand + eichel + gras + herz + schellen
        self._hand = sorted_hand

class RandomPlayer(Player):
    """Random Player"""
    def choose_game_mode(self, options, public_info):
        return (NO_GAME, None)

    def play_card(self, public_info, options=None):
        if options is None:
            card = random.choice(self._hand)
        else:
            card = random.choice(options)
        self._hand.remove(card)
        return card


class DummyPlayer(Player):
    """Always chooses specified game_mode if possible. Otherwise he passes.
       Always plays specified card if possible. Otherwise random card. For testing purpose only."""
    def __init__(self, name="Dummy", favorite_mode=None, favorite_cards=None):
        Player.__init__(self, name=name)
        self.favorite_mode = favorite_mode
        self.favorite_cards = favorite_cards

    def choose_game_mode(self, options, public_info):
        if self.favorite_mode in options:
            return self.favorite_mode
        else:
            chosen_mode = (NO_GAME, None)
            return chosen_mode

    def play_card(self, public_info, options=None):
        for fav_card in self.favorite_cards:
            if fav_card in options:
                card = fav_card
                break
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
