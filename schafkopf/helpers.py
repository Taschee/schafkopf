import random
from schafkopf.suits import BELLS, HEARTS, LEAVES, ACORNS, SUITS
from schafkopf.ranks import SEVEN, EIGHT, NINE, UNTER, OBER, KING, TEN, ACE, RANKS
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, WENZ, SOLO


def sort_hand(hand, trumpcards):
    trumps_in_hand = [trump for trump in trumpcards if trump in hand]
    bells = [(i, BELLS) for i in RANKS if (i, BELLS) in hand and (i, BELLS) not in trumpcards]
    hearts = [(i, HEARTS) for i in RANKS if (i, HEARTS) in hand and (i, HEARTS) not in trumpcards]
    leaves = [(i, LEAVES) for i in RANKS if (i, LEAVES) in hand and (i, LEAVES) not in trumpcards]
    acorns = [(i, ACORNS) for i in RANKS if (i, ACORNS) in hand and (i, ACORNS) not in trumpcards]
    sorted_hand = trumps_in_hand + acorns + leaves + hearts + bells
    return sorted_hand


def sample_opponent_hands(tricks, current_trick, trumpcards, playerindex, player_hand):
    opp_cards = opponent_cards_still_in_game(tricks, current_trick, player_hand)

    while True:
        random.shuffle(opp_cards)
        sample_hands = deal_player_hands(playerindex=playerindex, opp_cards=opp_cards,
                                         tricks=tricks, current_trick=current_trick, player_hand=player_hand)
        if card_distribution_possible(tricks, current_trick, trumpcards, playerindex, sample_hands):
            break

    return sample_hands


def sample_mode_proposals(public_info):
    deciding_players = {0, 1, 2, 3}
    current_player = public_info["leading_player_index"]
    mode_proposals = []
    min_mode = PARTNER_MODE
    # reconstruct possible mode proposals from public proposals
    for num in range(len(public_info["mode_proposals"])):
        public_proposal = public_info["mode_proposals"][num]
        # find proposing player
        while current_player not in deciding_players:
            current_player = (current_player + 1) % 4
        # if public proposal is NO_GAME
        if public_proposal == NO_GAME:
            deciding_players.remove(current_player)
            mode_proposals.append((NO_GAME, None))
        # otherwise: for first 4 proposals, only minimum game type is known
        elif num < 4:
            if min_mode == PARTNER_MODE:
                suit = random.choice([ACORNS, BELLS, LEAVES])
                mode_proposals.append((PARTNER_MODE, suit))
                min_mode += 1
            elif min_mode == WENZ:
                mode_proposals.append(random.choice([(WENZ, None)] + [(SOLO, suit) for suit in SUITS]))
                min_mode += 1
            else:
                mode_proposals.append(random.choice([(SOLO, suit) for suit in SUITS]))
        # after first proposals, the proposed game type is known, but not the suit
        else:
            if public_proposal == PARTNER_MODE:
                suit = random.choice([ACORNS, BELLS, LEAVES])
                mode_proposals.append((PARTNER_MODE, suit))
            elif public_proposal == WENZ:
                mode_proposals.append((WENZ, None))
            else:
                suit = random.choice(SUITS)
                mode_proposals.append((SOLO, suit))

    # check if bidding game finished, if yes, set last actual proposal to correct game mode
    if len(deciding_players) == 1 and len(public_info["mode_proposals"]) >= 4:
        for num in range(len(public_info["mode_proposals"]) - 1, -1, -1):
            proposal = public_info["mode_proposals"][num]
            if proposal != NO_GAME:
                mode_proposals[num] = public_info["game_mode"]
                break

    return mode_proposals


def opponent_cards_still_in_game(tricks, current_trick, player_hand):
    opp_cards = set([(i % 8, i // 8) for i in range(32)])
    not_possible_cards = player_hand + [card for card in current_trick.cards if card is not None]
    for trick in tricks:
        not_possible_cards += trick.cards
    for card in not_possible_cards:
        opp_cards.remove(card)
    return list(opp_cards)


def deal_player_hands(opp_cards, playerindex, player_hand, tricks, current_trick):
    opp_indices = list({0, 1, 2, 3})
    opp_indices.remove(playerindex)

    player_hands = [None, None, None, None]
    player_hands[playerindex] = player_hand

    for opp_index in opp_indices:

        number_of_cards = 8 - len(tricks)
        if current_trick.cards[opp_index] is not None:
            number_of_cards -= 1
        opp_hand = opp_cards[:number_of_cards]
        opp_cards = opp_cards[number_of_cards:]
        player_hands[opp_index] = opp_hand

    return player_hands


def didnt_follow_trump(tricks, current_trick, trumpcards, playerindex):
    for trick in tricks + [current_trick]:
        first_card = trick.cards[trick.leading_player_index]
        if first_card in trumpcards and first_card is not None:
            playercard = trick.cards[playerindex]
            if playercard not in trumpcards and playercard is not None:
                return True
    else:
        return False


def suits_not_followed(tricks, current_trick, trumpcards, playerindex):
    missing_suits = []
    for trick in tricks + [current_trick]:
        first_card = trick.cards[trick.leading_player_index]
        if first_card not in trumpcards and first_card is not None:
            suit = first_card[1]
            played_card = trick.cards[playerindex]
            if played_card is not None:
                if played_card[1] != suit:
                    missing_suits.append(suit)
    return missing_suits


def card_distribution_possible(tricks, current_trick, trumpcards, playerindex, player_hands):

    opp_indices = {0, 1, 2, 3}
    opp_indices.remove(playerindex)
    opp_indices = list(opp_indices)

    for opp_index in opp_indices:

        opp_cards = set(player_hands[opp_index])

        if didnt_follow_trump(tricks, current_trick, trumpcards, opp_index):
            if len(opp_cards & set(trumpcards)) > 0:
                return False

        for suit in suits_not_followed(tricks, current_trick, trumpcards, opp_index):
            for card in opp_cards:
                if card[1] == suit and card not in trumpcards:
                    return False

    return True


def define_trumpcards(game_mode):
    # trumpcards defined in order, lower index means stronger trump
    if game_mode[0] == PARTNER_MODE:
        trumpcards = [(OBER, i) for i in SUITS] + [(UNTER, i) for i in SUITS] \
                            + [(ACE, HEARTS), (TEN, HEARTS), (KING, HEARTS), (NINE, HEARTS), (EIGHT, HEARTS), (SEVEN, HEARTS)]
    elif game_mode[0] == WENZ:
        trumpcards = [(UNTER, i) for i in SUITS]
    elif game_mode[0] == SOLO:
        suit = game_mode[1]
        trumpcards = [(OBER, i) for i in SUITS] + [(UNTER, i) for i in SUITS] \
                            + [(ACE, suit), (TEN, suit), (KING, suit), (NINE, suit), (EIGHT, suit), (SEVEN, suit)]
    else:
        trumpcards = []
    return trumpcards
