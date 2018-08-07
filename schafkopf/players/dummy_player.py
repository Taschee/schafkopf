from schafkopf.players.player import Player
from schafkopf.game_modes import NO_GAME
import random


class DummyPlayer(Player):
    """Always chooses specified favorite game_mode if possible. Otherwise he passes.
       Always plays specified favorite cards if possible. Otherwise random card."""
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

