from schafkopf.game_modes import PARTNER_MODE, NO_GAME, WENZ, SOLO
from schafkopf.suits import BELLS, ACORNS, HEARTS, LEAVES
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, AS


class BiddingGame:
    def __init__(self, playerlist, leading_player_index):
        self.playerlist = playerlist
        self.deciding_players = set(playerlist)
        self.offensive_players = []
        self.current_player_index = leading_player_index
        self.game_mode = (NO_GAME, None)
        self.mode_proposals = []

    def get_current_player(self):
        return self.playerlist[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % 4

    def determine_possible_partnermodes(self, hand):
        possible_modes = set()
        for suit in [BELLS, LEAVES, ACORNS]:
            if (AS, suit) not in hand:
                for i in [SEVEN, EIGHT, NINE, KING, TEN]:
                    if (i, suit) in hand:
                        possible_modes.add((1, suit))
                        break
        return possible_modes

    def determine_possible_game_modes(self, hand, mode_to_beat=(NO_GAME, None)):
        possible_modes = {(NO_GAME, None)}
        if mode_to_beat[0] == NO_GAME:
            possible_modes |= self.determine_possible_partnermodes(hand) | {(WENZ, None), (SOLO, BELLS), (SOLO, HEARTS),
                                                                       (SOLO, LEAVES), (SOLO, ACORNS)}
        elif mode_to_beat[0] == PARTNER_MODE:
            possible_modes |= {(WENZ, None), (SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)}
        elif mode_to_beat[0] == WENZ:
            possible_modes |= {(SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)}
        return possible_modes

    def next_proposal(self):
        player = self.get_current_player()
        if player in self.deciding_players:
            options = self.determine_possible_game_modes(player.get_hand(), mode_to_beat=self.game_mode)
            chosen_mode = self.playerlist[self.current_player_index].choose_game_mode(options=options)
            if chosen_mode[0] <= self.game_mode[0]:
                self.deciding_players.remove(player)
            else:
                self.game_mode = chosen_mode
                self.offensive_players = [self.playerlist.index(player)]
        self.next_player()

    def finished(self):
        if len(self.deciding_players) == 1 and len(self.offensive_players) == 1 or len(self.deciding_players) == 0:
            return True
        else:
            return False

    def decide_game_mode(self):
        while not self.finished():
            self.next_proposal()
        if self.game_mode[0] == PARTNER_MODE:
            for player in self.playerlist:
                if (7, self.game_mode[1]) in player.get_hand():
                    self.offensive_players.append(self.playerlist.index(player))
