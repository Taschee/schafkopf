from schafkopf.game import Game

class Table:
    def __init__(self, player_list):
        self.player_list = player_list
        self.current_game = None
        self.previous_games = None
        self.scores = [0 for pl in player_list]