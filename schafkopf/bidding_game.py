from schafkopf.game_modes import PARTNER_MODE, NO_GAME, WENZ, SOLO
from schafkopf.suits import BELLS, ACORNS, HEARTS, LEAVES
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from copy import deepcopy


class BiddingGame:
    def __init__(self, playerlist, game_state):
        self.leading_player_index = game_state['leading_player_index']
        self.current_player_index = game_state['leading_player_index']
        self.playerlist = playerlist
        self.mode_proposals = game_state['mode_proposals']
        self.game_mode = game_state['game_mode']
        self.initialize_offensive_players(game_state)
        self.initialize_mode_to_beat(game_state)
        self.initialize_deciding_players(playerlist)

    def initialize_deciding_players(self, playerlist):
        self.deciding_players = set(range(len(playerlist)))
        for proposal in self.mode_proposals:
            while self.current_player_index not in self.deciding_players and len(self.deciding_players) > 0:
                self.next_player()
            if proposal == (NO_GAME, None):
                self.deciding_players.remove(self.current_player_index)
            self.next_player()

    def initialize_mode_to_beat(self, game_state):
        if len(self.mode_proposals) >= 4:
            self.mode_to_beat = game_state['game_mode'][0]
        else:
            self.mode_to_beat = sum([1 for mode in self.mode_proposals if mode[0] != NO_GAME])

    def initialize_offensive_players(self, game_state):
        self.offensive_players = [game_state['declaring_player']]
        if self.game_mode[0] == PARTNER_MODE:
            for player in self.playerlist:
                if (7, self.game_mode[1]) in player.starting_hand:
                    self.offensive_players.append(self.playerlist.index(player))
                    break

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
        # public mode proposals only contain game type (no suit). In first 4 proposals, only mininmum possible type

        mode_proposals_public = []
        mode_to_beat = 0
        for proposal in self.mode_proposals[:4]:
            if proposal[0] == NO_GAME:
                mode_proposals_public.append(0)
            else:
                mode_to_beat += 1
                mode_proposals_public.append(mode_to_beat)
        for proposal in self.mode_proposals[4:]:
            if proposal[0] == NO_GAME:
                mode_proposals_public.append(0)
            else:
                mode_proposals_public.append(proposal[0])
        # public game mode is minimum possible game type, no suit as well, if bidding game is not finished
        if self.finished():
            public_game_mode = self.game_mode
        else:
            public_game_mode = (self.mode_to_beat, None)
        return deepcopy({'leading_player_index': self.leading_player_index,
                         'current_player_index': self.current_player_index,
                         'mode_proposals': mode_proposals_public,
                         'declaring_player': self.offensive_players[0],
                         'game_mode': public_game_mode,
                         'trumpcards': [],
                         'tricks': [],
                         'current_trick': None})

    def next_proposal(self):
        while self.current_player_index not in self.deciding_players:
            self.next_player()
        player = self.get_current_player()
        options = self.determine_possible_game_modes(hand=player.get_hand(), mode_to_beat=self.mode_to_beat)
        public_info = self.get_public_info()

        chosen_mode = player.choose_game_mode(options=options, public_info=public_info)
        assert chosen_mode in options, 'Chosen mode was not legal'

        self.mode_proposals.append(chosen_mode)
        if chosen_mode[0] == NO_GAME:
            self.deciding_players.remove(self.current_player_index)
        else:
            # before all players made at least one proposal, mode to beat is just the number of actual game proposals
            if len(self.mode_proposals) < 4:
                self.mode_to_beat += 1
            # the first player making a public announcement has to propose at least a wenz now, if mode is not decided!
            elif len(self.mode_proposals) == 4:
                self.mode_to_beat = 1
                # if <= 1 actual proposals: game mode and offensive players are already decided
                if len(self.deciding_players) <= 1:
                    self.game_mode = max(self.mode_proposals, key=lambda x: x[0])
                    declaring_player = self.mode_proposals.index(self.game_mode)
                    self.offensive_players = self.set_offensive_players(declaring_player)
            # the chosen mode has to be higher then current game mode, if its not NO_GAME
            else:
                self.mode_to_beat = chosen_mode[0]
            self.game_mode = chosen_mode
            self.set_offensive_players(self.current_player_index)

        self.next_player()

    def set_offensive_players(self, playerindex):
        self.offensive_players = [playerindex]
        if self.game_mode[0] == PARTNER_MODE:
            for player in self.playerlist:
                if (7, self.game_mode[1]) in player.get_hand():
                    self.offensive_players.append(self.playerlist.index(player))

    def finished(self):
        if len(self.deciding_players) <= 1 and len(self.mode_proposals) >= 4:
            return True
        else:
            return False

    def play(self):
        while not self.finished():
            self.next_proposal()
