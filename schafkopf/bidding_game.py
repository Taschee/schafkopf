from schafkopf.game_modes import PARTNER_MODE, NO_GAME, WENZ, SOLO
from schafkopf.suits import BELLS, ACORNS, HEARTS, LEAVES
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from copy import deepcopy


class BiddingGame:
    def __init__(self, playerlist, game_state):
        self.leading_player_index = game_state["leading_player_index"]
        self.playerlist = playerlist
        self.game_mode = game_state["game_mode"]
        self.deciding_players = set(range(len(playerlist)))
        self.offensive_players = [game_state["declaring_player"]]
        if self.game_mode[0] == PARTNER_MODE:
            for player in self.playerlist:
                if (7, self.game_mode[1]) in player.get_hand():
                    self.offensive_players.append(self.playerlist.index(player))
                    break
        self.current_player_index = game_state["leading_player_index"]

        self.mode_proposals = game_state["mode_proposals"]
        # initializing deciding players
        for proposal in self.mode_proposals:
            while self.current_player_index not in self.deciding_players:
                self.next_player()
            if proposal == (NO_GAME, None):
                self.deciding_players.remove(self.current_player_index)
            self.next_player()


    def get_current_player(self):
        return self.playerlist[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % 4

    def determine_possible_partner_modes(self, hand):
        possible_modes = set()
        for suit in [BELLS, LEAVES, ACORNS]:
            if (ACE, suit) not in hand:
                for i in [SEVEN, EIGHT, NINE, KING, TEN]:
                    if (i, suit) in hand:
                        possible_modes.add((PARTNER_MODE, suit))
                        break
        return possible_modes

    def determine_possible_game_modes(self, hand, mode_to_beat=NO_GAME):
        possible_modes = {(NO_GAME, None)}
        if mode_to_beat == NO_GAME:
            possible_modes |= self.determine_possible_partner_modes(hand) | {(WENZ, None), (SOLO, BELLS),(SOLO, HEARTS),
                                                                             (SOLO, LEAVES), (SOLO, ACORNS)}
        elif mode_to_beat == PARTNER_MODE:
            possible_modes |= {(WENZ, None), (SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)}
        elif mode_to_beat == WENZ:
            possible_modes |= {(SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)}
        return possible_modes

    def get_public_info(self):
        return deepcopy({"leading_player_index": self.leading_player_index,
                         "current_player_index": self.current_player_index,
                         "mode_proposals": self.mode_proposals,
                         "declaring_player": self.offensive_players[0],
                         "game_mode": self.game_mode,
                         "trumpcards": [],
                         "tricks": [],
                         "current_trick": None})

    def next_proposal(self):
        while self.current_player_index not in self.deciding_players:
            self.next_player()
        player = self.get_current_player()
        mode_to_beat = sum([1 for proposal in self.mode_proposals if proposal[0] != NO_GAME])
        options = self.determine_possible_game_modes(hand=player.get_hand(), mode_to_beat=mode_to_beat)
        public_info = self.get_public_info()
        chosen_mode = player.choose_game_mode(options=options, public_info=public_info)
        if chosen_mode[0] == NO_GAME:
            self.deciding_players.remove(self.current_player_index)
        elif chosen_mode[0] > self.game_mode[0]:
            self.game_mode = chosen_mode
            self.set_offensive_players(player)
        self.mode_proposals.append(chosen_mode)
        self.next_player()

    def set_offensive_players(self, player):
        self.offensive_players = [self.playerlist.index(player)]
        if self.game_mode[0] == PARTNER_MODE:
            for player in self.playerlist:
                if (7, self.game_mode[1]) in player.get_hand():
                    self.offensive_players.append(self.playerlist.index(player))

    def finished(self):
        if (len(self.deciding_players) == 1 and self.game_mode[0] != NO_GAME) or len(self.deciding_players) == 0:
            return True
        else:
            return False

    def play(self):
        while not self.finished():
            self.next_proposal()
