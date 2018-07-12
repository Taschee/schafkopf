from copy import deepcopy
from  schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.helpers import define_trumpcards
from schafkopf.payouts import BASIC_PAYOUT_SOLO, BASIC_PAYOUT_PARTNER_MODE, EXTRA_PAYOUT
from schafkopf.bidding_game import BiddingGame
from schafkopf.trick_game import TrickGame


class Game:
    def __init__(self, players, game_state):
        self.playerlist = players
        self.leading_player_index = game_state[1]
        self.bidding_game = BiddingGame(playerlist=players, game_state=game_state)
        self.trick_game = TrickGame(playerlist=players, game_state=game_state)
        self.game_mode = (NO_GAME, None)
        self.winners = None

        for player, hand in zip(self.playerlist, game_state["player_hands"]):
            player.pick_up_cards(hand)

    def initialize_game_state(self, game_state):
        # a game state should be given by a dictionary:
        # {player_hands, leading_player_index, mode_proposals, tricks, current_trick}
        pass

    def initialize_game_mode(self, leading_player_index, mode_proposals):
        pass

    def find_offensive_partner(self, game_state):
        pass

    def initialize_scores(self, tricks):
        pass

    def play(self):
        if not self.bidding_game.finished():
            self.bidding_game.decide_game_mode()
        self.prepare_trick_game()
        if not self.trick_game.finished():
            self.trick_game.play()

    def prepare_trick_game(self):
        self.trick_game.offensive_players = self.bidding_game.offensive_players
        self.trick_game.mode_proposals = self.bidding_game.mode_proposals
        self.trick_game.game_mode = self.bidding_game.game_mode
        self.trick_game.trumpcards = define_trumpcards(self.trick_game.game_mode)

    def score_offensive_players(self):
        return sum([self.trick_game.scores[i] for i in self.trick_game.offensive_players])

    def determine_winners(self):
        if self.score_offensive_players() > 60:
            self.winners = self.trick_game.offensive_players
        else:
            self.winners = [pl for pl in range(len(self.playerlist)) if pl not in self.trick_game.offensive_players]
        return self.winners

    def get_payout(self, player):
        if self.trick_game.finished():
            if self.game_mode is NO_GAME:
                return 0
            else:
                if self.game_mode[0] == PARTNER_MODE:
                    return self.get_payout_partnermode(player)
                else:
                    return self.get_payout_solo(player)

    def schneider(self):
        offensive_score = self.score_offensive_players()
        if offensive_score > 90 or offensive_score < 31:
            return True
        else:
            return False

    def schwarz(self):
        trick_winners = [trick.winner for trick in self.trick_game.tricks]
        off_players = set(self.trick_game.offensive_players)
        num_offensive_tricks = 0
        for winner in trick_winners:
            if winner in off_players:
                num_offensive_tricks += 1
        if num_offensive_tricks == 0 or num_offensive_tricks == 8:
            return True
        else:
            return False

    def get_payout_partnermode(self, playerindex):
        payout = BASIC_PAYOUT_PARTNER_MODE
        if self.schneider():
            payout += EXTRA_PAYOUT
            if self.schwarz():
                payout += EXTRA_PAYOUT
        num_laufende = self.num_laufende()
        if num_laufende >= 3:
            payout += num_laufende * EXTRA_PAYOUT
        if playerindex in self.trick_game.offensive_players:
            if self.score_offensive_players() > 60:
                return payout
            else:
                return -payout
        else:
            if self.score_offensive_players() > 60:
                return -payout
            else:
                return payout

    def get_payout_solo(self, playerindex):
        payout = BASIC_PAYOUT_SOLO
        if self.schneider():
            payout += EXTRA_PAYOUT
            if self.schwarz():
                payout += EXTRA_PAYOUT
        num_laufende = self.num_laufende()
        if self.game_mode[0] == WENZ:
            if num_laufende >= 2:
                payout += num_laufende * EXTRA_PAYOUT
        else:
            if num_laufende >= 3:
                payout += num_laufende * EXTRA_PAYOUT
        if playerindex in self.trick_game.offensive_players:
            if self.score_offensive_players() > 60:
                return 3 * payout
            else:
                return -3 * payout
        else:
            if self.score_offensive_players() > 60:
                return -payout
            else:
                return payout

    def num_laufende(self):
        num = 1
        if self.player_with_highest_trump() in self.trick_game.offensive_players:
            team_with_laufende = self.trick_game.offensive_players
        else:
            team_with_laufende = [player for player in range(len(self.playerlist))
                                  if player not in self.trick_game.offensive_players]
        team_cards = self.get_teamcards(team_with_laufende)
        next_highest_trump_in_team = True
        while next_highest_trump_in_team:
            next_trump = self.trick_game.trumpcards[num]
            if next_trump in team_cards:
                num += 1
            else:
                next_highest_trump_in_team = False
        return num

    def player_with_highest_trump(self):
        highest_trump = self.trick_game.trumpcards[0]
        for player in self.playerlist:
            if highest_trump in player.get_starting_hand():
                return self.playerlist.index(player)

    def get_teamcards(self, team):
        teamcards = []
        for playerindex in team:
            player = self.playerlist[playerindex]
            teamcards += player.get_starting_hand()
        return teamcards
