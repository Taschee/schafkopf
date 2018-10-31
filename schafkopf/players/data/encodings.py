import numpy as np
from schafkopf.game_modes import SOLO, WENZ, PARTNER_MODE, NO_GAME
from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS
from schafkopf.helpers import sort_hand


def encode_one_hot_card(card):
    index = card[0] * 4 + card[1]
    encoded_card = np.zeros(32)
    encoded_card[index] = 1
    return encoded_card


def decode_one_hot_card(encoded_card):
    index = np.where(encoded_card == 1)[0][0]
    card_decoded = (index // 4, index % 4)
    return card_decoded


def encode_one_hot_hand(hand):
    hand = sort_hand(hand)
    enc_hand = np.zeros((len(hand), 32))
    for card, i in zip(hand, range(len(hand))):
        enc_hand[i] = encode_one_hot_card(card)
    return enc_hand


def encode_hand_inference(hand):
    enc_hand_one_hot = encode_one_hot_hand(hand)
    hand_encoded = np.sum(enc_hand_one_hot.transpose(), axis=1)
    return hand_encoded


def encode_one_hot_player_position(position):
    position_encoded = np.zeros(4)
    position_encoded[position] = 1
    return position_encoded


def decode_one_hot_player_position(position_encoded):
    return np.where(position_encoded == 1)[0][0]


def encode_one_hot_game_mode(game_mode, length=9):
    encoded_mode = np.zeros(length)
    if game_mode[0] == NO_GAME:
        encoded_mode[0] = 1
    elif game_mode[0] == PARTNER_MODE:
        if game_mode[1] == BELLS:
            encoded_mode[1] = 1
        elif game_mode[1] == LEAVES:
            encoded_mode[2] = 1
        elif game_mode[1] == ACORNS:
            encoded_mode[3] = 1
    elif game_mode[0] == WENZ:
        encoded_mode[4] = 1
    elif game_mode[0] == SOLO:
        shift = game_mode[1]
        encoded_mode[5 + shift] = 1
    return encoded_mode


def decode_one_hot_game_mode(game_mode_encoded):
    index = np.where(game_mode_encoded == 1)[0][0]
    game_mode = decode_mode_index(index)
    return game_mode


def decode_mode_index(index):
    if index == 0:
        game_mode = (NO_GAME, None)
    elif index == 1:
        game_mode = (PARTNER_MODE, BELLS)
    elif index == 2:
        game_mode = (PARTNER_MODE, LEAVES)
    elif index == 3:
        game_mode = (PARTNER_MODE, ACORNS)
    elif index == 4:
        game_mode = (WENZ, None)
    else:
        suit = index - 5
        game_mode = (SOLO, suit)
    return game_mode


def encode_played_cards(played_cards, next_rel_pos):
    """Takes list of tuples of (played_card, player) and next player to act as input.
    Outputs those encoded as (28, 36) numpy array."""
    seq = np.zeros((28, 36))

    if len(played_cards) == 0:
        rel_pos = next_rel_pos
        seq[0][32:] = encode_one_hot_player_position(rel_pos)
    else:
        # first entry contains only the relative player position of the player playing at the moment
        rel_pos = played_cards[0][1]
        seq[0][32:] = encode_one_hot_player_position(rel_pos)
        # after this, the next card and the relative player position of the next player are added to sequence
        for card_index in range(len(played_cards) - 1):
            card = played_cards[card_index][0]
            rel_pos_next_player = played_cards[card_index + 1][1]
            next_part_in_seq = np.zeros(36)
            next_part_in_seq[32:] = encode_one_hot_player_position(rel_pos_next_player)
            next_part_in_seq[:32] = encode_one_hot_card(card)
            seq[card_index + 1] = next_part_in_seq
        last_index = len(played_cards)
        last_card = played_cards[-1][0]
        last_part_in_seq = np.zeros(36)
        last_part_in_seq[32:] = encode_one_hot_player_position(next_rel_pos)
        last_part_in_seq[:32] = encode_one_hot_card(last_card)
        seq[last_index] = last_part_in_seq

    return seq
