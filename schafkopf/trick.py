from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, AS


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
            if card[0] == TEN:
                points += 10
            elif card[0] == UNTER:
                points += 2
            elif card[0] == OBER:
                points += 3
            elif card[0] == KING:
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
