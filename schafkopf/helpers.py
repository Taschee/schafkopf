import random

def sample_opponent_cards(game, player):
    opp_cards = opponent_cards_still_in_game(game, player)
    while True:
        random.shuffle(opp_cards)
        print("Opponent cards : ", opp_cards)
        if card_distribution_possible(game, player, opp_cards):
            break
    return opp_cards


def opponent_cards_still_in_game(game, player):
    opp_cards = []
    for opponent in game.get_players():
        if opponent != player:
            hand = opponent.get_hand()
            opp_cards += hand
    return opp_cards


def didnt_follow_trump(game, playerindex):
    trumpcards = game.get_trump_cards()
    for trick in game.get_tricks():
        first_card = trick.cards[trick.leading_player_index]
        if first_card in trumpcards:
            if trick.cards[playerindex] not in trumpcards:
                return True
    else:
        return False


def suits_not_followed(game, playerindex):
    missing_suits = []
    trumpcards = game.get_trump_cards()
    for trick in game.get_tricks():
        first_card = trick.cards[trick.leading_player_index]
        if first_card not in trumpcards:
            suit = first_card[1]
            if trick.cards[playerindex][1] != suit:
                missing_suits.append(suit)
    return missing_suits


def card_distribution_possible(game, player, opp_card_distribution):

    trumpcards = set(game.get_trump_cards())
    playerindex = game.get_players().index(player)
    opp_indices = [(playerindex + 1) % 4, (playerindex + 2) % 4, (playerindex + 3) % 4]

    for opp_index in opp_indices:

        opponent = game.get_players()[opp_index]
        number_of_cards = len(opponent.get_hand())
        opp_cards = set(opp_card_distribution[:number_of_cards])
        opp_card_distribution = opp_card_distribution[number_of_cards:]

        if didnt_follow_trump(game, opp_index):
            if len(opp_cards & trumpcards) > 0:
                print(" DIDNT FOLLOW TRUMP : ", opp_index)
                return False

        for suit in suits_not_followed(game, opp_index):
            for card in opp_cards:
                if card[1] == suit:
                    print(" DIDNT FOLLOW SUIT {} : ".format(suit), opp_index)
                    return False

    return True
