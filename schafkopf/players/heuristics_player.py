from schafkopf.players.player import Player
from schafkopf.ranks import OBER, UNTER, ACE, SEVEN, EIGHT, NINE, TEN, KING
from schafkopf.suits import HEARTS, LEAVES, ACORNS, BELLS, SUITS
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO
import random
import numpy as np

class HeuristicsPlayer(Player):

    def choose_game_mode(self, public_info, options):
        chosen_partner_mode = self.choose_partner_mode(options)
        chosen_wenz = self.choose_wenz(public_info)
        chosen_solo = self.choose_solo(public_info)
        chosen_mode = chosen_partner_mode
        if chosen_wenz[0] > chosen_mode[0]:
            chosen_mode = chosen_wenz
        if chosen_solo[0] > chosen_mode[0]:
            chosen_mode = chosen_solo
        return chosen_mode

    def play_card(self, public_info, options=None):
        pass

    def rank_in_hand(self, rank):
        return [card for card in self.hand if card[0] == rank]

    def suit_in_hand(self, suit):
        return [card for card in self.hand if card[0] not in {OBER, UNTER} and card[1] == suit]

    def choose_partner_mode(self, options):
        num_ober = len(self.rank_in_hand(OBER))
        num_unter = len(self.rank_in_hand(UNTER))
        num_hearts = len(self.suit_in_hand(HEARTS))

        if num_ober + num_unter + num_hearts >= 5:
            if num_ober >= 1:
                possible_partner_modes = [mode for mode in options if mode[0] == PARTNER_MODE]
                possible_suits = [mode[1] for mode in possible_partner_modes]
                chosen_suit = possible_suits[0]
                for suit in possible_suits[1:]:
                    if len(self.suit_in_hand(suit)) < len(self.suit_in_hand(chosen_suit)):
                        chosen_suit = suit
                return (PARTNER_MODE, chosen_suit)
            else:
                return (NO_GAME, None)

    def choose_wenz(self, public_info):
        num_unter = len(self.rank_in_hand(UNTER))
        aces_in_hand = self.rank_in_hand(ACE)
        num_aces = len(aces_in_hand)
        if num_unter >= 3:
            if num_aces >= 2:
                return (WENZ, None)
            elif num_aces == 1:
                suit_of_ace = aces_in_hand[0][1]
                if len(self.suit_in_hand(suit_of_ace)) >= 3:
                    return (WENZ, None)
                else:
                    return (NO_GAME, None)
        else:
            return (NO_GAME, None)

    def choose_solo(self, public_info):
        num_ober = len(self.rank_in_hand(OBER))
        num_unter = len(self.rank_in_hand(UNTER))

        if not self.enough_high_trumpcards():
            return (NO_GAME, None)

        else:
            num_suits = [len(self.suit_in_hand(suit)) for suit in SUITS.reverse()]
            trump_suit = np.argmax(num_suits)
            non_trumpcards = [card for card in self.hand if card[0] not in {UNTER, OBER} or card[1] == trump_suit]
            num_trump_suit = num_suits[trump_suit]
            num_trumpcards = num_ober + num_unter + num_trump_suit
            if num_trumpcards < 6:
                return (NO_GAME, None)

            sparrows = set(non_trumpcards)
            for card in sparrows:
                if card[0] == ACE:
                    sparrows.remove(card)
            if len(sparrows) >= 2:
                return (NO_GAME, None)
            elif len(sparrows) == 0:
                return (SOLO, trump_suit)

            else:
                if num_ober >= 3:
                    return (SOLO, trump_suit)
                elif num_unter + num_ober >= 5:
                    return (SOLO, trump_suit)
                elif num_ober + num_unter == 4 and len({(ACE, trump_suit), (TEN, trump_suit)} & self.hand) == 2:
                    return (SOLO, trump_suit)
                else:
                    return (NO_GAME, None)

    def enough_high_trumpcards(self):
        num_ober = len(self.rank_in_hand(OBER))
        num_unter = len(self.rank_in_hand(UNTER))
        if num_ober == 0 or (num_ober == 1 and self.rank_in_hand(OBER)[0][1] < LEAVES) or num_ober + num_unter < 3:
            return False
        else:
            return True




