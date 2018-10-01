import random
from schafkopf.game_modes import NO_GAME
from schafkopf.players.player import Player


class RandomPlayer(Player):
    """Random Player that never declares a game mode and randomly plays cards"""
    def choose_game_mode(self, options, public_info):
        return (NO_GAME, None)

    def play_card(self, public_info, options=None):
        if options is None:
            card = random.choice(self.hand)
        else:
            card = random.choice(options)
        self.hand.remove(card)
        return card

class FullyRandomPlayer(Player):
    """Also declares game mode randomly from the options"""
    def choose_game_mode(self, options, public_info):
        if options is None:
            chosen_mode = (NO_GAME, None)
        else:
            chosen_mode = random.choice(options)
        return chosen_mode

    def play_card(self, public_info, options=None):
        if options is None:
            card = random.choice(self.hand)
        else:
            card = random.choice(options)
        self.hand.remove(card)
        return card
