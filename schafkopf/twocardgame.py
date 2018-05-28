import random

cards = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1)]
trumpcards = [(3, 0), (2, 0), (1,0)]
NUMBER_OF_PLAYERS = 3

WEITER = 0
SOLOSPIEL = 1

class ThreePlayerTrick:
    def __init__(self, playerlist, leading_player):
        self.cards = [None for pl in playerlist]
        self.score = 0
        self.winner = None
        self.num_cards = 0
        self.leading_player_index = leading_player

    def calculate_points(self):
        self.score = sum([card[0] for card in self.cards])
        return self.score

    def determine_trickwinner(self):
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


class TwoCardGame:

    def __init__(self, players, leading_player_index=0, cards=cards):
        self._playerlist = players
        self._game_mode = (WEITER, None)
        self._trump_cards = trumpcards
        self._cards = cards
        self._num_tricks = len(cards) / len(players)
        self._deciding_players = set(players)
        self._offensive_players = []
        self._scores = [0 for player in self._playerlist]
        self._tricks = []
        self._current_trick = ThreePlayerTrick(players, leading_player_index)
        self._current_player_index = leading_player_index
        self._leading_player_index = leading_player_index
        self._winners = None

        random.shuffle(cards)
        number_of_cards = len(cards) // len(self._playerlist)
        for player in self._playerlist:
            player.pick_up_cards(cards[:number_of_cards])
            cards = cards[number_of_cards:]

    def next_player(self):
        self._current_player_index = (self._current_player_index + 1) % NUMBER_OF_PLAYERS

    def get_current_trick(self):
        return self._current_trick

    def get_current_playerindex(self):
        return self._current_player_index

    def get_trump_cards(self):
        return self._trump_cards

    def get_current_player(self):
        return self._playerlist[self._current_player_index]

    def get_players(self):
        return self._playerlist

    def get_tricks(self):
        return self._tricks

    def get_game_mode(self):
        return self._game_mode

    def next_proposed_game_mode(self):
        player = self._playerlist[self._current_player_index]
        if player in self._deciding_players:
            options = [(WEITER, None), (SOLOSPIEL, 0)]
            chosen_mode = self._playerlist[self._current_player_index].choose_game_mode(options=options)
            if chosen_mode[0] <= self._game_mode[0]:
                self._deciding_players.remove(player)
            else:
                self._game_mode = chosen_mode
                self._offensive_players = [self._playerlist.index(player)]
        self.next_player()

    def game_mode_decided(self):
        if len(self._deciding_players) == 1 and len(self._offensive_players) == 1 or len(self._deciding_players) == 0:
            self._current_player_index = self._leading_player_index
            return True
        else:
            return False

    def decide_game_mode(self):
        while not self.game_mode_decided():
            self.next_proposed_game_mode()

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
        self._current_trick = ThreePlayerTrick(self._playerlist, self._current_player_index)

    def play_next_card(self):
        current_player = self._playerlist[self._current_player_index]
        if self._current_trick.num_cards == 0:
            self._current_trick.leading_player_index = self._current_player_index
        options = self.possible_cards(self._current_trick, current_player.get_hand())
        next_card = current_player.play_card(previous_cards=self._current_trick.cards, options=options)
        self._current_trick.cards[self._current_player_index] = next_card
        self._current_trick.num_cards += 1

    def trick_finished(self):
        if self._current_trick.num_cards == 3:
            self._current_trick.calculate_points()
            self._current_trick.determine_trickwinner()
            self._current_player_index = self._current_trick.winner
            self._scores[self._current_player_index] += self._current_trick.score
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

    def score_offensive_players(self):
        return sum([self._scores[i] for i in self._offensive_players])

    def determine_winners(self):
        if self.score_offensive_players() > 6:
            self._winners = self._offensive_players
        else:
            self._winners = [pl for pl in range(len(self._playerlist)) if pl not in self._offensive_players]
        return self._winners



