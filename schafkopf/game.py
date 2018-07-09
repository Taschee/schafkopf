import random
from copy import deepcopy

SIEBEN = 0
ACHT = 1
NEUN = 2
UNTER = 3
OBER = 4
KOENIG = 5
ZEHN = 6
AS = 7

SCHELLEN = 0
HERZ = 1
GRAS = 2
EICHEL = 3
SUITS = [EICHEL, GRAS, HERZ, SCHELLEN]

# every game mode is a tuple (game_type, suit). possible game_types are:
WEITER = 0
RUFSPIEL = 1
WENZ = 2
SOLO = 3

BASIC_PAYOUT_RUFSPIEL = 20
BASIC_PAYOUT_SOLO = 50
EXTRA_PAYOUT = 10


def determine_possible_partnermodes(hand):
    possible_modes = set()
    for suit in [SCHELLEN, GRAS, EICHEL]:
        if (AS, suit) not in hand:
            for i in [SIEBEN, ACHT, NEUN, KOENIG, ZEHN]:
                if (i, suit) in hand:
                    possible_modes.add((1, suit))
                    break
    return possible_modes


def determine_possible_game_modes(hand, mode_to_beat=(WEITER, None)):
    possible_modes = {(WEITER, None)}
    if mode_to_beat[0] == WEITER:
        possible_modes |= determine_possible_partnermodes(hand) | {(WENZ, None), (SOLO, SCHELLEN), (SOLO, HERZ),
                                                                   (SOLO, GRAS), (SOLO, EICHEL)}
    elif mode_to_beat[0] == RUFSPIEL:
        possible_modes |= {(WENZ, None), (SOLO, SCHELLEN), (SOLO, HERZ), (SOLO, GRAS), (SOLO, EICHEL)}
    elif mode_to_beat[0] == WENZ:
        possible_modes |= {(SOLO, SCHELLEN), (SOLO, HERZ), (SOLO, GRAS), (SOLO, EICHEL)}
    return possible_modes


class Trick:
    def __init__(self, leading_player_index):
        self.cards = [None for player in range(4)]
        self.score = 0
        self.winner = None
        self.num_cards = 0
        self.leading_player_index = leading_player_index
        self.current_player = leading_player_index

    def __str__(self):
        return str(self.cards)

    def calculate_points(self):
        points = 0
        for card in self.cards:
            if card[0] == ZEHN:
                points += 10
            elif card[0] == UNTER:
                points += 2
            elif card[0] == OBER:
                points += 3
            elif card[0] == KOENIG:
                points += 4
            elif card[0] == AS:
                points += 11
        self.score = points
        return points

    def determine_trickwinner(self, trumpcards):
        # returns index of winning card / player
        trumps_in_trick = [card for card in self.cards if card in trumpcards]
        if len(trumps_in_trick) > 0:
            best_trump = min([trumpcards.index(trump) for trump in trumps_in_trick])
            self.winner = self.cards.index(trumpcards[best_trump])
        else:
            starting_index = self.leading_player_index
            first_card = self.cards[starting_index]
            played_suit = first_card[1]
            best_card = (max([i for (i, j) in self.cards if j == played_suit]), played_suit)
            self.winner = self.cards.index(best_card)


class Game:
    def __init__(self, players, leading_player_index=0, cards=[(i % 8, i // 8) for i in range(32)], shuffle_cards=True):
        self._playerlist = players
        self._game_mode = (WEITER, None)
        self._mode_proposals = [None for player in self._playerlist]
        self._trump_cards = []
        self._cards = cards
        self._max_num_tricks = len(cards) / len(players)
        self._deciding_players = set(players)
        self._offensive_players = []
        self._scores = [0 for player in self._playerlist]
        self._tricks = []
        self._current_trick = Trick(leading_player_index)
        self._current_player_index = leading_player_index
        self._leading_player_index = leading_player_index
        self._winners = None

        # deal cards
        if shuffle_cards:
            random.shuffle(cards)
        self._starting_deck = cards
        number_of_cards = len(cards) // len(self._playerlist)

        for player in self._playerlist:
            player.pick_up_cards(cards[:number_of_cards])
            cards = cards[number_of_cards:]

    def next_player(self):
        self._current_player_index = (self._current_player_index + 1) % 4

    def get_current_trick(self):
        return self._current_trick

    def get_current_playerindex(self):
        return self._current_player_index

    def get_trump_cards(self):
        return self._trump_cards

    def get_current_player(self):
        return self._playerlist[self._current_player_index]

    def get_current_player_index(self):
        return self._current_player_index

    def get_players(self):
        return self._playerlist

    def get_offensive_players(self):
        return self._offensive_players

    def get_tricks(self):
        return self._tricks

    def get_game_mode(self):
        return self._game_mode

    def set_game_mode(self, mode, offensive_players):
        self._game_mode = mode
        self._offensive_players = offensive_players

    def get_public_info(self):
        leading_player = deepcopy(self._leading_player_index)
        current_player = deepcopy(self._current_player_index)
        tricks = deepcopy(self._tricks)
        current_trick = deepcopy(self._current_trick)
        mode_proposals = deepcopy(self._mode_proposals)
        game_mode = deepcopy(self._game_mode)
        trumpcards = deepcopy(self._trump_cards)
        return {"leading_player_index": leading_player,
                "mode_proposals": mode_proposals,
                "game_mode": game_mode,
                "trumpcards": trumpcards,
                "tricks": tricks,
                "current_trick": current_trick,
                "current_player_index": current_player}

    def initialize_game_state(self, game_state):
        # a game state should be given by a dictionary:
        # {player_hands, leading_player_index, mode_proposals, tricks, current_trick}
        player_hands = game_state["player_hands"]
        leading_player_index = game_state["leading_player_index"]
        mode_proposals =  game_state["mode_proposals"]
        tricks = game_state["tricks"]
        current_trick = game_state["current_trick"]

        self._leading_player_index = leading_player_index
        self._mode_proposals = mode_proposals
        self.initialize_game_mode(leading_player_index, mode_proposals)
        if self.game_mode_decided():
            self.define_trumpcards()
            if self._game_mode[0] == RUFSPIEL:
                self.find_offensive_partner(game_state)
        self._tricks = tricks
        self.initialize_scores(tricks)
        self._current_trick = current_trick
        for player, hand in zip(self._playerlist, player_hands):
            player.pick_up_cards(hand)

    def initialize_game_mode(self, leading_player_index, mode_proposals):
        self._current_player_index = leading_player_index
        for proposal in mode_proposals:
            # find out who made the proposal
            while True:
                player = self.get_current_player()
                if player in self._deciding_players:
                    break
                else:
                    self.next_player()
            # change game mode according to proposal
            if proposal[0] <= self._game_mode[0]:
                self._deciding_players.remove(player)
            else:
                self._game_mode = proposal
                self._offensive_players = [self._playerlist.index(player)]
            self.next_player()

    def find_offensive_partner(self, game_state):
        player_hands = game_state[0]
        previous_tricks = game_state[3]
        current_trick = game_state[4]
        for playerindex in range(len(self._playerlist)):
            hand = player_hands[playerindex]
            for trick in previous_tricks:
                hand.append(trick.cards[playerindex])
            current_card = current_trick.cards[playerindex]
            if current_card is not None:
                hand.append(current_card)
            if (7, self._game_mode[1]) in hand:
                self._offensive_players.append(playerindex)
                break

    def initialize_scores(self, tricks):
        for trick in tricks:
            self._scores[trick.winner] += trick.score

    def next_proposed_game_mode(self):
        player = self.get_current_player()
        if player in self._deciding_players:
            options = determine_possible_game_modes(player.get_hand(), mode_to_beat=self._game_mode)
            chosen_mode = self._playerlist[self._current_player_index].choose_game_mode(options=options)
            if chosen_mode[0] <= self._game_mode[0]:
                self._deciding_players.remove(player)
            else:
                self._game_mode = chosen_mode
                self._offensive_players = [self._playerlist.index(player)]
        self.next_player()

    def game_mode_decided(self):
        if len(self._deciding_players) == 1 and len(self._offensive_players) == 1 or len(self._deciding_players) == 0:
            return True
        else:
            return False

    def decide_game_mode(self):
        while not self.game_mode_decided():
            self.next_proposed_game_mode()
        if self._game_mode[0] == RUFSPIEL:
            for player in self._playerlist:
                if (7, self._game_mode[1]) in player.get_hand():
                    self._offensive_players.append(self._playerlist.index(player))
        self.define_trumpcards()

    def define_trumpcards(self):
        # trumpcards defined in order, lower index means stronger trump
        if self._game_mode[0] == RUFSPIEL:
            self._trump_cards = [(OBER, i) for i in SUITS] + [(UNTER, i) for i in SUITS] \
                                + [(AS, HERZ), (ZEHN, HERZ), (KOENIG, HERZ), (NEUN, HERZ), (ACHT, HERZ), (SIEBEN, HERZ)]
        elif self._game_mode[0] == WENZ:
            self._trump_cards = [(UNTER, i) for i in SUITS]
        elif self._game_mode[0] == SOLO:
            suit = self._game_mode[1]
            self._trump_cards = [(OBER, i) for i in SUITS] + [(UNTER, i) for i in SUITS] \
                                + [(AS, suit), (ZEHN, suit), (KOENIG, suit), (NEUN, suit), (ACHT, suit), (SIEBEN, suit)]

    def suit_in_hand(self, suit, hand):
        suit_cards = [card for card in hand if card[1] == suit and card not in self._trump_cards]
        if len(suit_cards) > 0:
            return suit_cards
        else:
            return hand

    def possible_cards(self, current_trick, hand):
        if current_trick.num_cards == 0:
            if self._game_mode[0] == RUFSPIEL and (7, self._game_mode[1]) in hand:
                forbidden_cards = [card for card in hand if card not in self._trump_cards
                                and card[1] == self._game_mode[1] and card[0] != 7]
                return [card for card in hand if card not in forbidden_cards]
            else:
                return hand
        else:
            first_card = current_trick.cards[current_trick.leading_player_index]
        if first_card in self._trump_cards:
            players_trumpcards = [trump for trump in self._trump_cards if trump in hand]
            if len(players_trumpcards) > 0:
                return players_trumpcards
            else:
                return hand
        elif self._game_mode[0] == RUFSPIEL and first_card[1] == self._game_mode[1] and (7, self._game_mode[1]) in hand:
            return (7,self._game_mode[1])
        else:
            suit = first_card[1]
            return self.suit_in_hand(suit, hand)

    def reset_current_trick(self):
        self._tricks.append(self._current_trick)
        self._current_trick = Trick(self._current_player_index)

    def play_next_card(self):
        if len(self._tricks) == 0 and self._current_trick.cards[self._leading_player_index] is None:
            self._current_player_index = self._leading_player_index
        current_player = self.get_current_player()
        if self._current_trick.num_cards == 0:
            self._current_trick.leading_player_index = self._current_player_index
        options = self.possible_cards(self._current_trick, current_player.get_hand())
        info = self.get_public_info()
        next_card = current_player.play_card(public_info=info, options=options)
        self._current_trick.cards[self._current_player_index] = next_card
        self._current_trick.num_cards += 1

    def trick_finished(self):
        if self._current_trick.num_cards == 4:
            self._current_trick.calculate_points()
            self._current_trick.determine_trickwinner(self._trump_cards)
            self._current_player_index = self._current_trick.winner
            self._scores[self._current_player_index] += self._current_trick.score
            self.reset_current_trick()
        else:
            self.next_player()

    def get_last_trick(self):
        return self._tricks[-1]

    def finished(self):
        if len(self._tricks) == self._max_num_tricks:
            return True
        else:
            return False

    def score_offensive_players(self):
        return sum([self._scores[i] for i in self._offensive_players])

    def determine_winners(self):
        if self.score_offensive_players() > 60:
            self._winners = self._offensive_players
        else:
            self._winners = [pl for pl in range(len(self._playerlist)) if pl not in self._offensive_players]
        return self._winners

    def get_payout(self, player):
        if self.finished():
            if self._game_mode is WEITER:
                return 0
            else:
                if self._game_mode[0] == RUFSPIEL:
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
        trick_winners = {trick.winner for trick in self._tricks}
        off_players = set(self._offensive_players)
        num_off_tricks = len(trick_winners & off_players)
        if num_off_tricks == 0 or num_off_tricks == 8:
            return True
        else:
            return False

    def get_payout_partnermode(self, playerindex):
        payout = BASIC_PAYOUT_RUFSPIEL
        if self.schneider():
            payout += EXTRA_PAYOUT
            if self.schwarz():
                payout += EXTRA_PAYOUT
        num_laufende = self.num_laufende()
        if num_laufende >= 3:
            payout += num_laufende * EXTRA_PAYOUT
        if playerindex in self._offensive_players:
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
        if self._game_mode[0] == WENZ:
            if num_laufende >= 2:
                payout += num_laufende * EXTRA_PAYOUT
        else:
            if num_laufende >= 3:
                payout += num_laufende * EXTRA_PAYOUT
        if playerindex in self._offensive_players:
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
        if self.player_with_highest_trump() in self._offensive_players:
            team_with_laufende = self._offensive_players
        else:
            team_with_laufende = [player for player in range(len(self._playerlist))
                                  if player not in self._offensive_players]
        team_cards = self.get_teamcards(team_with_laufende)
        next_highest_trump_in_team = True
        while next_highest_trump_in_team:
            next_trump = self._trump_cards[num]
            if next_trump in team_cards:
                num += 1
            else:
                next_highest_trump_in_team = False
        return num

    def player_with_highest_trump(self):
        highest_trump = self._trump_cards[0]
        for player in self._playerlist:
            if highest_trump in player.get_starting_hand():
                return self._playerlist.index(player)

    def get_teamcards(self, team):
        teamcards = []
        for playerindex in team:
            player = self._playerlist[playerindex]
            teamcards += player.get_starting_hand()
        return teamcards
