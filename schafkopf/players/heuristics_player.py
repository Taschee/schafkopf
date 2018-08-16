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
        if len(options) == 1:
            return options[0]
        else:
            if public_info["game_mode"][0] == PARTNER_MODE:
                chosen_card = self.choose_card_partner_mode(public_info, options)
            elif public_info["game_mode"][0] == WENZ:
                chosen_card = self.choose_card_wenz(public_info, options)
            else:
                chosen_card = self.choose_card_solo(public_info, options)
            self.hand.remove(chosen_card)
            return chosen_card

    def rank_in_hand(self, rank):
        return [card for card in self.hand if card[0] == rank]

    def suit_in_hand(self, suit, wenz=False):
        if not wenz:
            return [card for card in self.hand if card[0] not in {OBER, UNTER} and card[1] == suit]
        else:
            return [card for card in self.hand if card[0] != UNTER and card[1] == suit]

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
                if len(self.suit_in_hand(suit_of_ace, wenz=True)) >= 3:
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

    def choose_card_partner_mode(self, public_info, options):
        position_in_list = public_info["current_trick"].current_player_index
        if position_in_list == public_info["declaring_player"]:
            return self.choose_card_partner_mode_declarer(public_info, options)
        elif (ACE, public_info["game_mode"][1]) in self.starting_hand:
            return self.choose_card_partner_mode_partner(public_info, options)
        else:
            return self.choose_card_partner_mode_defensive(public_info, options)

    def choose_card_wenz(self, public_info, options):
        position_in_list = public_info["current_trick"].current_player_index
        if position_in_list in public_info["declaring_player"]:
            pass
        else:
            pass

    def choose_card_solo(self, public_info, options):
        position_in_list = public_info["current_trick"].current_player_index
        if position_in_list in public_info["declaring_player"]:
            pass
        else:
            pass

    def choose_card_partner_mode_declarer(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_partner_mode_declarer(public_info)
        else:
            return self.follow_suit_partner_mode_declarer(public_info, options)

    def choose_card_partner_mode_partner(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_partner_mode_partner(public_info)
        else:
            return self.follow_suit_partner_mode_partner(public_info, options)

    def choose_card_partner_mode_defensive(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_partner_mode_defensive(public_info, options)
        else:
            return self.follow_suit_partner_mode_defensive(public_info, options)

    def lead_trick_partner_mode_declarer(self, public_info):
        trumpcards_in_hand = [card for card in public_info["trumpcards"] if card in self.hand]
        played_trumpcards = self.previously_played_trumpcards(public_info)
        # check if other players have still trumpcards. play trumpcard if yes, no trumpcard otherwise
        if len(trumpcards_in_hand + played_trumpcards) < 14:
            return random.choice(trumpcards_in_hand)
        else:
            aces = self.aces_in_hand(public_info)
            if len(aces) > 0:
                return random.choice(aces)
            else:
                return random.choice([card for card in self.hand if card not in trumpcards_in_hand])

    def follow_suit_partner_mode_declarer(self, public_info, options):
        leading_player = public_info["leading_player_index"]
        leading_card = public_info["current_trick"].cards[leading_player]
        trumpcards_in_hand = [card for card in public_info["trumpcards"] if card in self.hand]
        if leading_card not in public_info["trump_cards"]:
            suit =  leading_card[1]
            # play ACE if possible
            if (ACE, suit) in options:
                return (ACE, suit)
            # if played suit is not in hand, play low trump
            elif len([card for card in self.hand if card[1] == suit and card not in public_info["trumpcards"]]) == 0:
                return trumpcards_in_hand[-1]
            else:
                return random.choice(options)
        else:
            return random.choice(trumpcards_in_hand)

    def lead_trick_partner_mode_partner(self, public_info):
        trumpcards_in_hand = [card for card in public_info["trumpcards"] if card in self.hand]
        played_trumpcards = self.previously_played_trumpcards(public_info)
        # check if other players have still trumpcards. play highest trumpcard if yes, no trumpcard otherwise
        if len(trumpcards_in_hand + played_trumpcards) < 14:
            return trumpcards_in_hand[0]
        else:
            aces = self.aces_in_hand(public_info)
            if len(aces) > 0:
                return random.choice(aces)
            else:
                return random.choice([card for card in self.hand if card not in trumpcards_in_hand])

    def follow_suit_partner_mode_partner(self, public_info, options):
        leading_player = public_info["leading_player_index"]
        first_card = public_info["current_trick"].cards[leading_player]
        best_trumpcard_in_game = self.best_trumpcard_in_game(public_info)
        if first_card in public_info["trumpcars"]:
            if leading_player == public_info["declaring_player"]:
                if first_card == best_trumpcard_in_game:
                    if (ACE, HEARTS) in options:
                        return (ACE, HEARTS)
                    elif len([card for card in options if card[0] == TEN]) > 0:
                        return random.choice([card for card in options if card[0] == TEN])
                    elif (KING, HEARTS) in options:
                        return (KING, HEARTS)
                    else:
                        return random.choice(options)
                else:
                    if best_trumpcard_in_game in options:
                        return best_trumpcard_in_game
                    else:
                        return random.choice(options)
            else:
                return random.choice(options)
        else:
            if (ACE, first_card[1]) in options:
                return (ACE, first_card[1])
            else:
                return random.choice(options)

    def previously_played_trumpcards(self, public_info):
        played_trumpcards = []
        for trick in public_info["tricks"]:
            played_trumpcards += [card for card in trick.cards if card in public_info["trumpcards"]]
        return played_trumpcards

    def best_trumpcard_in_game(self, public_info):
        played_trumpcards = self.previously_played_trumpcards(public_info)
        return [card for card in public_info["trumpcards"] if card not in played_trumpcards][0]

    def aces_in_hand(self, public_info):
        return [card for card in self.hand if card[0] == ACE and card not in public_info["trumpcards"]]

    def lead_trick_partner_mode_defensive(self, public_info, options):
        first_cards = [trick.cards[trick.leading_player_index] for trick in public_info["tricks"]]
        # check if the offensive partner was searched for
        partner_found = False
        for card in first_cards:
            if card not in public_info["trumpcards"] and card[1] == public_info["game_mode"][1]:
                partner_found = True
                break
        # if not: search, if possible
        if not partner_found:
            searching_cards = self.suit_in_hand(public_info["game_mode"][1])
            # if searching isn't possible, play ACE if possible
            if len(searching_cards) == 0:
                aces = self.aces_in_hand(public_info)
                if len(aces) > 0:
                    return random.choice(aces)
                else:
                    return random.choice(options)
            # if taking the searched ACE trick seems likely, search with card with most points
            elif len(searching_cards) >= 3:
                return max(searching_cards, key=lambda x: x[0])
            else:
                return random.choice(searching_cards)
        else:
            # play ACE, if possible
            aces = self.aces_in_hand(public_info)
            if len(aces) > 0:
                return random.choice(aces)
            else:
                return random.choice(options)

    def follow_suit_partner_mode_defensive(self, public_info, options):
        leading_player = public_info["leading_player_index"]
        first_card = public_info["current_trick"].cards[leading_player]
        first_cards = [trick.cards[trick.leading_player_index] for trick in public_info["tricks"]]
        # if trump was played, play randomly
        if first_card in public_info["trumpcards"]:
            return random.choice(options)
        # if searched suit is played
        elif first_card[1] == public_info["game_mode"][1]:
            # check if the offensive partner was searched for
            partner_found = False
            for card in first_cards:
                if card not in public_info["trumpcards"] and card[1] == public_info["game_mode"][1]:
                    partner_found = True
                    break
            # if not: take the trick if possible with a trumpcard
            if not partner_found:
                searching_suit = self.suit_in_hand(public_info["game_mode"][1])
                if len(searching_suit) == 0:
                    trumps_in_hand = [card for card in public_info["trumpcards"] if card in self.hand]
                    # if there are still trumps in own hand, take the trick
                    if len(trumps_in_hand) > 0:
                        if (ACE, HEARTS) in self.hand:
                            return (ACE, HEARTS)
                        elif (TEN, HEARTS) in self.hand:
                            return (TEN, HEARTS)
                        elif (KING, HEARTS) in self.hand:
                            return (KING, HEARTS)
                        else:
                            return trumps_in_hand[-1]
                    # else: low points card
                    else:
                        return min(options, key=lambda x: x[0])
                else:
                    # if player has to follow, do so with lowest card in searched suit
                    return min(options, key=lambda x: x[0])
            else:
                return random.choice(options)

        else:
            # in case of other suit: follow with ACE if possible
            if (ACE, first_card[1]) in self.hand:
                return (ACE, first_card[1])
            else:
                return random.choice(options)








