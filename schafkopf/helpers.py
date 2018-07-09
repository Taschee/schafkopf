import random


def sample_opponent_hands(tricks, current_trick, trumpcards, playerindex, player_hand):
    opp_cards = opponent_cards_still_in_game(tricks, current_trick, player_hand)

    while True:
        random.shuffle(opp_cards)
        sample_hands = deal_player_hands(playerindex=playerindex, opp_cards=opp_cards,
                                         tricks=tricks, current_trick=current_trick, player_hand=player_hand)
        if card_distribution_possible(tricks, current_trick, trumpcards, playerindex, sample_hands):
            break

    return sample_hands


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
            if played_card[1] != suit and played_card is not None:
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
