from schafkopf.game import Game
from schafkopf.card_deck import CardDeck
from schafkopf.game_modes import NO_GAME, WENZ, PARTNER_MODE, SOLO
from schafkopf.suits import SUITS


class Tournament:
    def __init__(self, playerlist, number_of_games=32, record_games=True):
        self.playerlist = playerlist
        self.number_of_games = number_of_games
        self.game_number = 1
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
                      "declaring_player": None,
                      "tricks": [],
                      "current_trick": None,
                      "possible_actions": [(NO_GAME, None), (WENZ, None)] +
                                          [(PARTNER_MODE, suit) for suit in SUITS] +
                                          [(SOLO, suit) for suit in SUITS]}
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
        self.game_number += 1

    def play(self):
        while not self.finished():
            self.play_next_game()

    def finished(self):
        if self.game_number <= self.number_of_games:
            return False
        else:
            return True

    def get_tournament_results(self):
        return self.cumulative_rewards

    def get_game_results(self):
        if self.record_games:
            return [game.get_payouts() for game in self.games]
