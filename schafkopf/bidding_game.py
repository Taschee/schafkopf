from schafkopf.game_modes import PARTNER_MODE, NO_GAME, WENZ, SOLO
from schafkopf.suits import BELLS, ACORNS, HEARTS, LEAVES
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE


class BiddingGame:
    def __init__(self, playerlist, game_state):
        self.playerlist = playerlist
        for player, hand in zip(self.playerlist, game_state["player_hands"]):
            player.pick_up_cards(hand)
        self.deciding_players = set(playerlist)
        self.offensive_players = game_state["offensive_players"]
        self.current_player_index = game_state["leading_player_index"]
        self.game_mode = game_state["game_mode"]
        self.mode_proposals = game_state["mode_proposals"]
        # initializing deciding players
        for proposal in self.mode_proposals:
            player = self.playerlist[self.current_player_index]
            while player not in self.deciding_players:
                self.next_player()
                player = self.playerlist[self.current_player_index]
            if proposal == (NO_GAME, None):
                self.deciding_players.remove(player)
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

    def determine_possible_game_modes(self, hand, mode_to_beat=(NO_GAME, None)):
        possible_modes = {(NO_GAME, None)}
        if mode_to_beat[0] == NO_GAME:
            possible_modes |= self.determine_possible_partner_modes(hand) | {(WENZ, None), (SOLO, BELLS),(SOLO, HEARTS),
                                                                             (SOLO, LEAVES), (SOLO, ACORNS)}
        elif mode_to_beat[0] == PARTNER_MODE:
            possible_modes |= {(WENZ, None), (SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)}
        elif mode_to_beat[0] == WENZ:
            possible_modes |= {(SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)}
        return possible_modes

    def next_proposal(self):
        player = self.get_current_player()
        while player not in self.deciding_players:
            self.next_player()
            player = self.get_current_player()
        options = self.determine_possible_game_modes(player.get_hand(), mode_to_beat=self.game_mode)
        chosen_mode = player.choose_game_mode(options=options)
        if chosen_mode == (NO_GAME, None):
            self.deciding_players.remove(player)
        else:
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
        if len(self.deciding_players) == 1 and len(self.offensive_players) in {1,2} or len(self.deciding_players) == 0:
            return True
        else:
            return False

    def decide_game_mode(self):
        while not self.finished():
            self.next_proposal()
