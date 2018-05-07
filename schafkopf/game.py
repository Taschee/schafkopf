
import random

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

WEITER = 0
RUFSPIEL = 1
WENZ = 2
SOLO = 3


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

def calculate_points(trick):
    points = 0
    for card in trick["cards"]:
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
    return points

class Trick:
    def __init__(self, playerlist, leading_player):
        self.cards = [None for player in playerlist]
        self.score = []
        self.winner = None
        self.num_cards = 0
        self.leading_player_index = leading_player
        self.current_player = leading_player

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
    def __init__(self, players, leading_player_index=0, cards=[(i % 8, i // 8) for i in range(32)]):
        self._playerlist = players
        self._game_mode = (WEITER, None)
        self._trump_cards = []
        self._cards = cards
        self._num_tricks = len(cards) / len(players)
        self._deciding_players = set(players)
        self._offensive_players = []
        self._scores = [0 for player in self._playerlist]
        self._tricks = []
        self._current_trick = Trick(players, leading_player_index)
        self._current_player_index = leading_player_index
        self._leading_player_index = leading_player_index

        # deal cards
        random.shuffle(cards)
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

    def get_current_player(self):
        return  self._playerlist[self._current_player_index]

    def get_tricks(self):
        return self._tricks

    def next_proposed_game_mode(self):
        player = self._playerlist[self._current_player_index]
        if player in self._deciding_players:
            options = determine_possible_game_modes(player.get_hand(), mode_to_beat=self._game_mode)
            chosen_mode = self._playerlist[self._current_player_index].choose_game_mode(options=options)
            if chosen_mode[0] <= self._game_mode[0]:
                self._deciding_players.remove(player)
            else:
                self._game_mode = chosen_mode
                self._offensive_players = [player]
        self.next_player()

    def game_mode_decided(self):
        if len(self._deciding_players) == 1 and len(self._offensive_players) == 1:
            self._current_player_index = self._leading_player_index
            return True
        else:
            return False

    def decide_game_mode(self):
        while not self.game_mode_decided():
            self.next_proposed_game_mode()
        if self._game_mode[0] == 1:
            for player in self._playerlist:
                if (7, self._game_mode[1]) in player.get_hand():
                    self._offensive_players.append(player)
        self.define_trumpcards()

    def get_game_mode(self):
        return self._game_mode

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
            return hand
        else:
            first_card = current_trick.cards[current_trick.leading_player_index]
        if first_card in self._trump_cards:
            players_trumpcards = [trump for trump in self._trump_cards if trump in hand]
            if len(players_trumpcards) > 0:
                return players_trumpcards
            else:
                return hand
        else:
            suit = first_card[1]
            return self.suit_in_hand(suit, hand)

    def reset_current_trick(self):
        self._tricks.append(self._current_trick)
        self._current_trick = Trick(self._playerlist, self._current_player_index)

    def play_next_card(self):
        current_player = self._playerlist[self._current_player_index]
        if self._current_trick.num_cards == 0:
            self._current_trick.leading_player_index = self._current_player_index
        options = self.possible_cards(self._current_trick, current_player.get_hand())
        next_card = current_player.play_card(previous_cards=self._current_trick.cards, options=options)
        self._current_trick.cards[self._current_player_index] = next_card
        self._current_trick.num_cards += 1

    def trick_finished(self):
        if self._current_trick.num_cards == 4:
            self._current_trick.determine_trickwinner(self._trump_cards)
            self._current_player_index = self._current_trick.winner
            self.reset_current_trick()
        else:
            self.next_player()

    def get_last_trick(self):
        return self._tricks[-1]

    def finished(self):
        if len(self._tricks) == self._num_tricks:
            return True
        else:
            return False
