from schafkopf.game import Game
from schafkopf.card_deck import CardDeck
from schafkopf.game_modes import NO_GAME


class Tournament:
    def __init__(self, playerlist, number_of_games=32, record_games=True):
        self.playerlist = playerlist
        self.number_of_games = number_of_games
        self.leading_player_index = 0
        self.record_games = record_games
        self.cumulative_rewards = [0 for player in self.playerlist]
        if record_games:
            self.games = []

    def update_leading_player_index(self):
        self.leading_player_index = (self.leading_player_index + 1) % 4

    def deal_cards(self):
        card_deck = CardDeck()
        card_deck.shuffle()
        return card_deck.deal_player_hands()

    def prepare_new_game(self):
        player_hands = self.deal_cards()
        game_state = {"player_hands": player_hands,
                      "leading_player_index": self.leading_player_index,
                      "mode_proposals": [],
                      "game_mode": (NO_GAME, None),
                      "offensive_players": [],
                      "tricks": [],
                      "current_trick": None}
        return Game(players=self.playerlist, game_state=game_state)

    def play_next_game(self):
        game = self.prepare_new_game()
        game.play()
        if self.record_games:
            self.games.append(game)
        for playerindex in range(len(self.playerlist)):
            reward = game.get_payout(playerindex)
            self.cumulative_rewards[playerindex] += reward
        self.update_leading_player_index()

    def play_tournament(self):
        for game_num in range(self.number_of_games):
            self.play_next_game()
