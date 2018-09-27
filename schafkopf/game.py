from copy import deepcopy
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
from schafkopf.helpers import define_trumpcards
from schafkopf.payouts import BASIC_PAYOUT_SOLO, BASIC_PAYOUT_PARTNER_MODE, EXTRA_PAYOUT
from schafkopf.bidding_game import BiddingGame
from schafkopf.trick_game import TrickGame


class Game:
    def __init__(self, players, game_state):
        state = deepcopy(game_state)
        self.playerlist = players
        for player, hand in zip(self.playerlist, state['player_hands']):
            player.pick_up_cards(hand)
            previous_tricks = deepcopy(state['tricks'])
            if state['current_trick'] is not None:
                previous_tricks += [state['current_trick']]
            player.set_starting_hand(hand, previous_tricks, self.playerlist.index(player))
        self.leading_player_index = state['leading_player_index']
        self.bidding_game = BiddingGame(playerlist=players, game_state=state)
        self.trick_game = TrickGame(playerlist=players, game_state=state)
        self.winners = None

    def get_current_player(self):
        if not self.bidding_game.finished():
            return self.bidding_game.current_player_index
        else:
            return self.trick_game.current_player_index

    def get_public_info(self):
        if not self.bidding_game.finished():
            return self.bidding_game.get_public_info()
        else:
            return self.trick_game.get_public_info()

    def get_game_state(self):
        game_state = self.get_public_info()
        game_state['game_mode'] = self.bidding_game.game_mode
        game_state['mode_proposals'] = self.bidding_game.mode_proposals
        game_state['player_hands'] = [player.get_hand() for player in self.playerlist]
        game_state['possible_actions'] = self.get_possible_actions()
        return deepcopy(game_state)

    def get_possible_actions(self):
        if self.bidding_game.finished():
            return self.trick_game.possible_cards(current_trick=self.trick_game.current_trick,
                                                  hand=self.trick_game.get_current_player().get_hand())
        else:
            hand = self.bidding_game.get_current_player().get_hand()
            mode_to_beat = self.bidding_game.mode_to_beat
            return self.bidding_game.determine_possible_game_modes(hand=hand,
                                                                   mode_to_beat=mode_to_beat)

    def next_action(self):
        if not self.bidding_game.finished():
            self.bidding_game.next_proposal()
            if self.bidding_game.finished():
                self.prepare_trick_game()
        elif not self.trick_game.finished():
            self.trick_game.play_next_card()
            self.trick_game.trick_finished()

    def play(self):
        if not self.bidding_game.finished():
            self.bidding_game.play()
            self.prepare_trick_game()
        if not self.trick_game.finished():
            self.trick_game.play()

    def finished(self):
        if self.bidding_game.finished():
            if self.bidding_game.game_mode == (NO_GAME, None):
                return True
            else:
                return self.trick_game.finished()
        else:
            return False

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

    def get_payouts(self):
        if self.trick_game.finished():
            return [self.get_payout(playerindex) for playerindex in range(len(self.playerlist))]

    def get_payout(self, player):
        if self.trick_game.game_mode[0] is NO_GAME:
            return 0
        else:
            if self.trick_game.game_mode[0] == PARTNER_MODE:
                return self.get_payout_partner_mode(player)
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

    def get_payout_partner_mode(self, playerindex):
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
        if self.trick_game.game_mode[0] == WENZ:
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
        while next_highest_trump_in_team and num < len(self.trick_game.trumpcards):
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
