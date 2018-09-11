from schafkopf.ranks import OBER, UNTER


def switch_card_suit(card, suit, new_suit, wenz=False):
    if not wenz:
        if card[1] == suit and card[0] not in {OBER, UNTER}:
            transformed_card = (card[0], new_suit)
        elif card[1] == new_suit and card[0] not in {OBER, UNTER}:
            transformed_card = (card[0], suit)
        else:
            transformed_card = card[:]
    else:
        if card[1] == suit and card[0] != UNTER:
            transformed_card = (card[0], new_suit)
        elif card[1] == new_suit and card[0] != UNTER:
            transformed_card = (card[0], suit)
        else:
            transformed_card = card[:]
    return transformed_card


def switch_suits_played_cards(played_cards, game_suit, new_suit):
    return [(switch_card_suit(card, game_suit, new_suit), player) for card, player in played_cards]


def switch_suits_player_hands(player_hands, game_suit, new_suit):
    hands_transformed = []
    for hand in player_hands:
        transformed_hand = [switch_card_suit(card, game_suit, new_suit) for card in hand]
        hands_transformed.append(transformed_hand)
    return hands_transformed
