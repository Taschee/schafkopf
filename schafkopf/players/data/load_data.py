import pickle
import random
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


def prepare_data_trickplay(game_data_dic, num_samples=1):

    played_cards = game_data_dic['played_cards']

    card_sequences = []
    cards_to_predict = []

    # create num_samples different sequences from one game
    seq_lenghts = random.sample(range(27), num_samples)

    for seq_len in seq_lenghts:
        new_seq = np.zeros((28, 36))
        # first entry contains only the relative player position of the player playing at the moment
        rel_pos = played_cards[0][1]
        new_seq[0][32:] = enc.encode_one_hot_player_position(rel_pos)
        # after this, the next card and the relative player position of the next player are added to sequence
        for card_index in range(seq_len):
            card = played_cards[card_index][0]
            rel_pos_next_player = played_cards[card_index + 1][1]
            train_example = np.zeros(36)
            train_example[32:] = enc.encode_one_hot_player_position(rel_pos_next_player)
            train_example[:32] = enc.encode_one_hot_card(card)
            new_seq[card_index + 1] = train_example
        card_sequences.append(new_seq)

        next_card = played_cards[seq_len][0]
        cards_to_predict.append(enc.encode_one_hot_card(next_card))

    return card_sequences, cards_to_predict


def load_data_trickplay(file, num_samples=1):

    num_games = num_games_in_file(file)

    with open(file, 'rb') as infile:

        x_data = np.zeros(shape=(num_games * num_samples, 28, 36))
        y_data = np.zeros(shape=(num_games * num_samples, 32))

        for game_num in range(num_games):
            game_data_dic = pickle.load(infile)
            card_sequences, cards_to_predict = prepare_data_trickplay(game_data_dic, num_samples)
            for num in range(num_samples):
                x = card_sequences[num]
                y = cards_to_predict[num]
                x_data[game_num * num_samples + num] = x
                y_data[game_num * num_samples + num] = y

    return x_data, y_data

print(num_games_in_file('train_data.p'))
print(num_games_in_file('train_data_partner.p'))
print(num_games_in_file('train_data_solo.p'))
print(num_games_in_file('train_data_wenz.p'))