import random


def sample_opponent_cards(tricks, current_trick, trumpcards, playerindex, player_hand):
    opp_cards = opponent_cards_still_in_game(tricks, current_trick, player_hand)
    while True:
        random.shuffle(opp_cards)
        print("Opponent cards : ", opp_cards)
        if card_distribution_possible(tricks, current_trick, trumpcards, playerindex, opp_cards):
            break
    return opp_cards


def opponent_cards_still_in_game(tricks, current_trick, player_hand):
    opp_cards = set([(i % 8, i // 8) for i in range(32)])
    not_possible_cards = player_hand + current_trick.cards
    for trick in tricks:
        not_possible_cards += trick.cards
    for card in not_possible_cards:
        opp_cards.remove(card)
    return list(opp_cards)


def didnt_follow_trump(tricks, current_trick, trumpcards, playerindex):
    for trick in tricks + [current_trick]:
        first_card = trick.cards[trick.leading_player_index]
        if first_card in trumpcards:
            if trick.cards[playerindex] not in trumpcards:
                return True
    else:
        return False


def suits_not_followed(tricks, current_trick, trumpcards, playerindex):
    missing_suits = []
    for trick in tricks + [current_trick]:
        first_card = trick.cards[trick.leading_player_index]
        if first_card not in trumpcards:
            suit = first_card[1]
            if trick.cards[playerindex][1] != suit:
                missing_suits.append(suit)
    return missing_suits


def card_distribution_possible(tricks, current_trick, trumpcards, playerindex, opp_card_distribution):

    opp_indices = list({0, 1, 2, 3}.remove(playerindex))

    for opp_index in opp_indices:

        number_of_cards = 8 - len(tricks)
        if current_trick.cards[opp_index] is not None:
            number_of_cards -= 1
        opp_cards = set(opp_card_distribution[:number_of_cards])
        opp_card_distribution = opp_card_distribution[number_of_cards:]

        if didnt_follow_trump(tricks, current_trick, trumpcards, opp_index):
            if len(opp_cards & trumpcards) > 0:
                return False

        for suit in suits_not_followed(tricks, current_trick, trumpcards, opp_index):
            for card in opp_cards:
                if card[1] == suit:
                    return False

    return True
