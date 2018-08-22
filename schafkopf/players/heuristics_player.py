from schafkopf.players.player import Player
from schafkopf.ranks import OBER, UNTER, ACE, SEVEN, EIGHT, NINE, TEN, KING, RANKS
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

    def play_card(self, public_info, options):
        if len(options) == 1:
            card = options[0]
            self.hand.remove(card)
            return card
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
        # if at least 5 trumpcards, 1 OBER: play partnermode if possible
        if num_ober + num_unter + num_hearts >= 5 and num_ober >= 1:
            possible_partner_modes = [mode for mode in options if mode[0] == PARTNER_MODE]
            if len(possible_partner_modes) > 0:
                possible_suits = [mode[1] for mode in possible_partner_modes]
                chosen_suit = possible_suits[0]
                for suit in possible_suits[1:]:
                    if len(self.suit_in_hand(suit)) < len(self.suit_in_hand(chosen_suit)):
                        chosen_suit = suit
                return (PARTNER_MODE, chosen_suit)
            else:
                return (NO_GAME, None)
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
        else:
            return (NO_GAME, None)

    def choose_solo(self, public_info):
        num_ober = len(self.rank_in_hand(OBER))
        num_unter = len(self.rank_in_hand(UNTER))

        if not self.enough_high_trumpcards():
            return (NO_GAME, None)

        else:
            suits = SUITS[:]
            suits.reverse()
            num_suits = [len(self.suit_in_hand(suit)) for suit in suits]
            trump_suit = np.argmax(num_suits)
            non_trumpcards = [card for card in self.hand if card[0] not in {UNTER, OBER} or card[1] == trump_suit]
            num_trump_suit = num_suits[trump_suit]
            num_trumpcards = num_ober + num_unter + num_trump_suit
            if num_trumpcards < 6:
                return (NO_GAME, None)

            sparrows = [card for card in non_trumpcards if card[0] != ACE]

            if len(sparrows) >= 2:
                return (NO_GAME, None)
            elif len(sparrows) == 0:
                return (SOLO, trump_suit)

            else:
                if num_ober >= 3:
                    return (SOLO, trump_suit)
                elif num_unter + num_ober >= 5:
                    return (SOLO, trump_suit)
                elif num_ober + num_unter == 4 and len({(ACE, trump_suit), (TEN, trump_suit)} & self.hand) >= 1:
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
        if position_in_list == public_info["declaring_player"]:
            return self.choose_card_wenz_declarer(public_info, options)
        else:
            return self.choose_card_wenz_defensive(public_info, options)

    def choose_card_solo(self, public_info, options):
        position_in_list = public_info["current_trick"].current_player_index
        if position_in_list == public_info["declaring_player"]:
            return self.choose_card_solo_declarer(public_info, options)
        else:
            return self.choose_card_solo_defensive(public_info, options)

    def choose_card_partner_mode_declarer(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_partner_mode_declarer(public_info, options)
        else:
            return self.follow_suit_partner_mode_declarer(public_info, options)

    def choose_card_partner_mode_partner(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_partner_mode_partner(public_info, options)
        else:
            return self.follow_suit_partner_mode_partner(public_info, options)

    def choose_card_partner_mode_defensive(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_partner_mode_defensive(public_info, options)
        else:
            return self.follow_suit_partner_mode_defensive(public_info, options)

    def lead_trick_partner_mode_declarer(self, public_info, options):
        trumpcards_in_hand = self.trumpcards_in_hand(public_info)
        non_trumpcards_in_hand = [card for card in self.hand if card not in trumpcards_in_hand]
        played_trumpcards = self.previously_played_trumpcards(public_info)
        # check if other players have still trumpcards. play trumpcard if yes, no trumpcard otherwise
        if len(trumpcards_in_hand) + len(played_trumpcards) < 14:
            if len(trumpcards_in_hand) > 0:
                return random.choice(trumpcards_in_hand)
            else:
                return random.choice(options)
        else:
            aces = self.aces_in_hand(public_info)
            if len(aces) > 0:
                return random.choice(aces)
            elif len(non_trumpcards_in_hand) > 0:
                return random.choice(non_trumpcards_in_hand)
            else:
                return random.choice(options)

    def follow_suit_partner_mode_declarer(self, public_info, options):
        current_trick = public_info["current_trick"]
        leading_player = current_trick.leading_player_index
        leading_card = current_trick.cards[leading_player]
        trumpcards_in_hand = self.trumpcards_in_hand(public_info)
        if leading_card not in public_info["trumpcards"]:
            suit = leading_card[1]
            # play ACE if possible
            if (ACE, suit) in options:
                return (ACE, suit)
            # if played suit is not in hand, play low trump
            elif len([card for card in self.hand if card[1] == suit and card not in public_info["trumpcards"]]) == 0:
                if len(trumpcards_in_hand) > 0:
                    return trumpcards_in_hand[-1]
                else:
                    return random.choice(options)
            else:
                return random.choice(options)
        else:
            if len(trumpcards_in_hand) > 0:
                return random.choice(trumpcards_in_hand)
            else:
                return random.choice(options)

    def lead_trick_partner_mode_partner(self, public_info, options):
        trumpcards_in_hand = self.trumpcards_in_hand(public_info)
        played_trumpcards = self.previously_played_trumpcards(public_info)
        # check if other players have still trumpcards. play highest trumpcard if yes, no trumpcard otherwise
        if len(trumpcards_in_hand + played_trumpcards) < 14:
            if len(trumpcards_in_hand) > 0:
                return trumpcards_in_hand[0]
            else:
                return random.choice(options)
        else:
            aces = self.aces_in_hand(public_info)
            if len(aces) > 0:
                return random.choice(aces)
            else:
                return random.choice([card for card in self.hand if card not in trumpcards_in_hand])

    def follow_suit_partner_mode_partner(self, public_info, options):
        leading_player = public_info["current_trick"].leading_player_index
        first_card = public_info["current_trick"].cards[leading_player]
        best_trumpcard_in_game = self.best_trumpcard_still_in_game(public_info)
        if first_card in public_info["trumpcards"]:
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
        played_trumpcards = [card for card in public_info["current_trick"].cards if card in public_info["trumpcards"]]
        for trick in public_info["tricks"]:
            played_trumpcards += [card for card in trick.cards if card in public_info["trumpcards"]]
        return played_trumpcards

    def best_trumpcard_still_in_game(self, public_info):
        played_trumpcards = self.previously_played_trumpcards(public_info)
        trumpcards_left = [card for card in public_info["trumpcards"] if card not in played_trumpcards]
        if len(trumpcards_left) > 0:
            return trumpcards_left[0]
        else:
            return None

    def aces_in_hand(self, public_info):
        return [card for card in self.hand if card[0] == ACE and card not in public_info["trumpcards"]]

    def lead_trick_partner_mode_defensive(self, public_info, options):
        # check if the offensive partner was searched for
        # if not: search, if possible
        if not self.partner_found(public_info):
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

    def partner_found(self, public_info):
        first_cards = [trick.cards[trick.leading_player_index] for trick in public_info["tricks"]]
        partner_found = False
        for card in first_cards:
            if card not in public_info["trumpcards"] and card[1] == public_info["game_mode"][1]:
                partner_found = True
                break
        return partner_found

    def follow_suit_partner_mode_defensive(self, public_info, options):
        leading_player = public_info["current_trick"].leading_player_index
        first_card = public_info["current_trick"].cards[leading_player]
        # if trump was played, play randomly
        if first_card in public_info["trumpcards"]:
            return random.choice(options)
        # if searched suit is played
        elif first_card[1] == public_info["game_mode"][1]:
            # check if the offensive partner was searched for
            # if not: take the trick if possible with a trumpcard
            if not self.partner_found(public_info):
                searching_suit_in_hand = self.suit_in_hand(public_info["game_mode"][1])
                if len(searching_suit_in_hand) == 0:
                    trumps_in_hand = self.trumpcards_in_hand(public_info)
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

    def choose_card_wenz_declarer(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_wenz_declarer(public_info, options)
        else:
            return self.follow_trick_wenz_declarer(public_info, options)

    def lead_trick_wenz_declarer(self, public_info, options):
        unter_in_hand = self.trumpcards_in_hand(public_info)
        unter_played = self.rank_played(UNTER, public_info)
        # check if there are still opponent UNTER, if yes, play highest own UNTER
        if len(unter_in_hand + unter_played) < 4:
            return unter_in_hand[0]
        # play sparrow if there are no opponent UNTER left (if possible)
        else:
            sparrows = self.sparrows_in_hand(public_info)
            if len(sparrows) > 0:
                return random.choice(sparrows)
            else:
                return random.choice(options)

    def rank_played(self, rank, public_info):
        rank_played = []
        for trick in public_info["tricks"]:
            rank_in_trick = [card for card in trick.cards if card[0] == rank]
            rank_played += rank_in_trick
        return rank_played

    def follow_trick_wenz_declarer(self, public_info, options):
        leading_player = public_info["current_trick"].leading_player_index
        first_card = public_info["current_trick"].cards[leading_player]
        unter_in_hand = self.rank_in_hand(UNTER)
        if first_card not in public_info["trumpcards"]:
            best_card_left = self.best_suitcard_left(first_card[1], public_info)
            # play highest card of the suit if possible
            if best_card_left in options:
                return best_card_left
            # if suit is not in hand, play lowest unter
            elif len(self.suit_in_hand(first_card[1], wenz=True)) == 0:
                if len(unter_in_hand) > 0:
                    return min(unter_in_hand, key=lambda x: x[1])
                else:
                    return random.choice(options)
            else:
                return random.choice(options)
        else:
            best_trumpcard = self.best_trumpcard_still_in_game(public_info)
            if best_trumpcard in options:
                return best_trumpcard
            else:
                return random.choice(options)

    def card_played_before(self, card, public_info):
        played_cards = public_info["current_trick"].cards[:]
        for trick in public_info["tricks"]:
            played_cards += trick.cards
        if card in played_cards:
            return True
        else:
            return False

    def best_suitcard_left(self, suit, public_info):
        played_cards = public_info["current_trick"].cards[:]
        for trick in public_info["tricks"]:
            played_cards += trick.cards
        if public_info["game_mode"] != WENZ:
            suit_cards_left = [(rank, suit) for rank in [ACE, TEN, KING, NINE, EIGHT, SEVEN]]
        else:
            suit_cards_left = [(rank, suit) for rank in [ACE, TEN, KING, OBER, NINE, EIGHT, SEVEN]]
        for card in played_cards:
            if card in suit_cards_left:
                suit_cards_left.remove(card)
        if len(suit_cards_left) > 0:
            return suit_cards_left[0]
        else:
            return None

    def choose_card_wenz_defensive(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_wenz_defensive(public_info, options)
        else:
            return self.follow_trick_wenz_defensive(public_info, options)

    def lead_trick_wenz_defensive(self, public_info, options):
        max_suit = self.longest_suit(public_info)
        if (ACE, max_suit) in options:
            return (ACE, max_suit)
        else:
            return random.choice(self.suit_in_hand(max_suit))

    def longest_suit(self, public_info):
        suits = SUITS[:]
        suits.reverse()
        if public_info["game_mode"][0] != WENZ:
            suit_nums = [len(self.suit_in_hand(suit, wenz=True)) for suit in suits]
            return np.argmax(suit_nums)
        else:
            suit_nums = [len(self.suit_in_hand(suit)) for suit in suits]
            return np.argmax(suit_nums)

    def follow_trick_wenz_defensive(self, public_info, options):
        current_trick = public_info["current_trick"]
        leading_player = current_trick.leading_player_index
        first_card = current_trick.cards[leading_player]
        offensive_player = public_info["declaring_player"]
        trumpcards_in_hand = [card for card in public_info["trumpcards"] if card in self.hand]
        low_cards_in_hand = self.rank_in_hand(SEVEN) + self.rank_in_hand(EIGHT) + self.rank_in_hand(NINE)

        # if a UNTER was played:
        if first_card in public_info["trumpcards"]:
            # if the offensive player played the best trumpcard left, go with lowest trumpcard or card with few points
            if current_trick.cards[offensive_player] == self.best_trumpcard_still_in_game(public_info):
                if len(trumpcards_in_hand) > 0:
                    return trumpcards_in_hand[-1]
                elif len(low_cards_in_hand) > 0:
                    return random.choice(low_cards_in_hand)
                else:
                    return random.choice(options)
            # random non-ace otherwise
            else:
                aces = self.aces_in_hand(public_info)
                non_aces = [card for card in self.hand if card not in aces]
                return random.choice(non_aces)

        else:
            # in case of no UNTER as first card: play best suitcard if possible, or if possible, use UNTER to take trick
            if len(self.suit_in_hand(first_card[1], wenz=True)) > 0:
                best_suitcard = self.best_suitcard_left(first_card[1], public_info)
                if best_suitcard in options:
                    return best_suitcard
                else:
                    return random.choice(options)
            else:
                unter_in_hand = self.rank_in_hand(UNTER)
                if len(unter_in_hand) == 0:
                    return random.choice(options)
                else:
                    return unter_in_hand[-1]

    def choose_card_solo_declarer(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_solo_declarer(public_info, options)
        else:
            return self.follow_trick_solo_declarer(public_info, options)

    def lead_trick_solo_declarer(self, public_info, options):
        best_trump_left = self.best_trumpcard_still_in_game(public_info)
        previously_played_trumpcards = self.previously_played_trumpcards(public_info)
        trumpcards_in_hand = [card for card in public_info["trumpcards"] if card in self.hand]
        # if opponents still have trumpcards:
        if len(previously_played_trumpcards + trumpcards_in_hand) < 14:
            # play best trumpcard left if possible, random trumpcard otherwise
            if best_trump_left in options:
                return best_trump_left
            else:
                return random.choice(trumpcards_in_hand)
        # play ACE or sparrow otherwise if possible
        else:
            aces = self.aces_in_hand(public_info)
            sparrows = self.sparrows_in_hand(public_info)
            if len(aces) > 0:
                return random.choice(aces)
            elif len(sparrows) > 0:
                return random.choice(sparrows)
            else:
                return random.choice(options)

    def follow_trick_solo_declarer(self, public_info, options):
        leading_player = public_info["current_trick"].leading_player_index
        first_card = public_info["current_trick"].cards[leading_player]
        solo_suit = public_info["game_mode"][1]
        if first_card in public_info["trumpcards"]:
            best_trumpcard_left = self.best_trumpcard_still_in_game(public_info)
            if best_trumpcard_left in options:
                return best_trumpcard_left
            else:
                return [card for card in public_info["trumpcards"] if card in self.hand][-1]
        else:
            played_suit_cards_in_hand = self.suit_in_hand(first_card[1])
            if len(played_suit_cards_in_hand) > 0:
                best_card = self.best_suitcard_left(first_card[1], public_info)
                if best_card in options:
                    return best_card
                else:
                    return random.choice(options)
            else:
                if not self.suit_played_before(first_card[1], public_info):
                    if (ACE, solo_suit) in options:
                        return (ACE, solo_suit)
                    elif (TEN, solo_suit) in options:
                        return (TEN, solo_suit)
                    elif (KING, solo_suit) in options:
                        return (KING, solo_suit)
                    else:
                        return self.trumpcards_in_hand(public_info)[-1]
                else:
                    return random.choice(self.trumpcards_in_hand(public_info))

    def sparrows_in_hand(self, public_info):
        sparrows = []
        for card in self.hand:
            if (ACE, card[1]) not in self.hand and card not in public_info["trumpcards"]:
                sparrows.append(card)
        return sparrows

    def trumpcards_in_hand(self, public_info):
        return [card for card in public_info["trumpcards"] if card in self.hand]

    def suit_played_before(self, suit, public_info):
        played_before = False
        for trick in public_info["tricks"]:
            first_card = trick.cards[trick.leading_player_index]
            if first_card[1] == suit:
                played_before = True
                break
        return played_before

    def choose_card_solo_defensive(self, public_info, options):
        if public_info["current_trick"].num_cards == 0:
            return self.lead_trick_solo_defensive(public_info, options)
        else:
            return self.follow_trick_solo_defensive(public_info, options)

    def lead_trick_solo_defensive(self, public_info, options):
        aces = self.aces_in_hand(public_info)
        if len(aces) > 0:
            return random.choice(aces)
        else:
            non_trumpcards = [card for card in self.hand if card not in self.trumpcards_in_hand(public_info)]
            return random.choice(non_trumpcards)

    def follow_trick_solo_defensive(self, public_info, options):
        current_trick = public_info["current_trick"]
        leading_player = current_trick.leading_player_index
        offensive_player = public_info["declaring_player"]
        first_card = current_trick.cards[leading_player]
        trumpcards_in_hand = self.trumpcards_in_hand(public_info)
        low_cards = self.rank_in_hand(SEVEN) + self.rank_in_hand(EIGHT) + self.rank_in_hand(NINE)
        if leading_player == offensive_player:
            # play lowest trumpcard or zero points if player played highest trump
            if first_card == self.best_trumpcard_still_in_game(public_info):
                if len(trumpcards_in_hand) > 0:
                    return trumpcards_in_hand[-1]
                else:
                    if len(low_cards) > 0:
                        return random.choice(low_cards)
                    else:
                        return random.choice(options)
            elif first_card in public_info["trumpcards"]:
                return random.choice(options)
            elif first_card[0] == self.best_suitcard_left(first_card[1], public_info):
                if len(self.suit_in_hand(first_card[0])) > 0:
                    return min(options, key=lambda x: x[0])
                else:
                    if len(trumpcards_in_hand) > 0:
                        return random.choice(trumpcards_in_hand)
                    elif len(low_cards) > 0:
                        return random.choice(low_cards)
                    else:
                        return random.choice(options)
            # in case of sparrow, maximum points
            else:
                return max(options, key=lambda x: x[0])
        else:
            if first_card not in public_info["trumpcards"]:
                best_card = self.best_suitcard_left(first_card[1], public_info)
                if best_card in options:
                    if current_trick.cards[offensive_player] not in public_info["trumpcards"]:
                        return best_card
                    else:
                        return min(options, key=lambda x: x[0])
                else:
                    return random.choice(options)
            elif first_card == self.best_trumpcard_still_in_game(public_info):
                return max(options, key=lambda x: x[0])
            elif self.best_trumpcard_still_in_game(public_info) in options:
                return self.best_trumpcard_still_in_game(public_info)
            else:
                return random.choice(options)
