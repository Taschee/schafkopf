from schafkopf.monte_carlo import MCTree, MCNode
from schafkopf.helpers import sample_opponent_cards
from schafkopf.players import Player, RandomPlayer
from schafkopf.game import Game
import random

class AIPlayer(Player):

    def next_action(self):

    def search(self):
        pass

    def selection(self):
        pass

    def expand(self):
        pass

    def simulation(self):
        pass


    def choose_game_mode(self, options):
        return random.choice(tuple(options))

    def play_card(self, public_info, options=None):
        # choose card by sampling opponent cards N times, in each sample perform MonteCarloSimulation, return best card
        # ! paralizing possile !



        return
