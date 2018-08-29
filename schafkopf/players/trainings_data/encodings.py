import numpy as np
from schafkopf.game_modes import SOLO, WENZ, PARTNER_MODE, NO_GAME
from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS


def encode_one_hot_card(card):
    index = card[0] * 4 + card[1]
    encoded_card = np.zeros(32)
    encoded_card[index] = 1
    return encoded_card


def decode_one_hot_card(encoded_card):
    index = np.where(encoded_card == 1)[0][0]
    return (index // 4, index % 4)


def encode_one_hot_player_position(position):
    position_encoded = np.zeros(32)
    position_encoded[position] = 1
    return position_encoded


def decode_one_hot_player_position(position_encoded):
    return np.where(position_encoded == 1)[0][0]


def encode_one_hot_game_mode(game_mode):
    encoded_mode = np.zeros(9)
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
