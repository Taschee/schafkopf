from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE


class Trick:
    def __init__(self, leading_player_index, score=0, winner=None, cards=None):
        self.score = score
        self.winner = winner
        self.leading_player_index = leading_player_index
        self.current_player_index = leading_player_index
        self.num_cards = 0
        if cards is None:
            self.cards = [None for player in range(4)]
        else:
            self.cards = cards
            for card in cards:
                if card is not None:
                    self.current_player_index = (self.current_player_index + 1) % 4
                    self.num_cards += 1

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return "< " + str(self.cards) + " >"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def calculate_points(self):
        points = 0
        for card in self.cards:
            if card is not None:
                if card[0] == TEN:
                    points += 10
                elif card[0] == UNTER:
                    points += 2
                elif card[0] == OBER:
                    points += 3
                elif card[0] == KING:
                    points += 4
                elif card[0] == ACE:
                    points += 11
        self.score = points
        return points

    def determine_trickwinner(self, trumpcards):
        # determines index of winning card / player
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

    def finished(self):
        if self.num_cards == 4:
            return True
        else:
            return False
