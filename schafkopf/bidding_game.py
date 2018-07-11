from schafkopf.game_modes import PARTNER_MODE, NO_GAME, WENZ, SOLO
from schafkopf.helpers import determine_possible_game_modes


class BiddingGame:
    def __init__(self, playerlist, leading_player_index):
        self.playerlist = playerlist
        self.deciding_players = set(playerlist)
        self.offensive_players = []
        self.leading_player_index = leading_player_index
        self.current_player_index = leading_player_index
        self.game_mode = (NO_GAME, None)
        self.mode_proposals = []

    def get_current_player(self):
        return self.playerlist[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % 4

    def next_proposal(self):
        player = self.get_current_player()
        if player in self.deciding_players:
            options = determine_possible_game_modes(player.get_hand(), mode_to_beat=self.game_mode)
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
