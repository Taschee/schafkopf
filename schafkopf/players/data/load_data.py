import pickle
import numpy as np
from schafkopf.game_modes import NO_GAME
import schafkopf.players.data.encodings as enc


def num_games_in_file(file):
    with (open(file, "rb")) as openfile:
        num = 0
        while True:
            try:
                pickle.load(openfile)
                num += 1
            except EOFError:
                break
        return num


def prepare_data_bidding(game_data_dic):

    player_hands = game_data_dic['player_hands']
    game_mode = game_data_dic['game_mode']
    declaring_player = game_data_dic['declaring_player']

    data_list = []

    for hand, player_pos in zip(player_hands, range(4)):
        x = np.zeros(shape=(8, 32))

        for card, index in zip(hand, range(8)):
            card_encoded = enc.encode_one_hot_card(card)
            x[index] = card_encoded

        if player_pos == declaring_player:
            y = enc.encode_one_hot_game_mode(game_mode)
        else:
            y = enc.encode_one_hot_game_mode((NO_GAME, None))

        data_list.append((x, y))

    return data_list


def load_data_bidding(file):

    num_games = num_games_in_file(file)

    with open(file, 'rb') as infile:

        x_data = np.zeros(shape=(num_games * 4, 8, 32))
        y_data = np.zeros(shape=(num_games * 4, 9))

        for game_num in range(num_games):
            game_data_dic = pickle.load(infile)
            data_list = prepare_data_bidding(game_data_dic)
            for hand_num in range(4):
                x, y = data_list[hand_num]
                x_data[game_num * 4 + hand_num] = x
                y_data[game_num * 4 + hand_num] = y

    return x_data, y_data


def prepare_data_trickplay(game_data_dic):

    game_mode = game_data_dic['game_mode']
    declaring_player = game_data_dic['declaring_player']
    played_cards = game_data_dic['played_cards']

    card_sequences = []

    # want to predict the next card up to the 28th card.
    # first column in a sequence is no card, only the declaring player and whose turn it is !!!!!!!!????!!!!
    for seq_len in range(28):
        new_seq = np.zeros((29, 40))
        new_seq[0][32:] = enc.encode_one_hot_player_position(declaring_player)
        for card_index in range(seq_len):
            card = played_cards[card_index][0]
            train_example = np.zeros(36) ## whose turn it is / leading player as well?
            train_example[32:] = enc.encode_one_hot_player_position(declaring_player)
            train_example[:32] = enc.encode_one_hot_card(card)
            new_seq[card_index + 1] = train_example
        card_sequences.append(new_seq)

    return card_sequences


