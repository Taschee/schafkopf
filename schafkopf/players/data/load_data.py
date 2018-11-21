import pickle
import random
import numpy as np
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, SOLO, WENZ
from schafkopf.players.data.data_processing import switch_suits_player_hands
import schafkopf.players.data.encodings as enc
from schafkopf.suits import SUITS, BELLS, LEAVES, ACORNS


def num_games_in_file(file):
    with (open(file, "rb")) as file:
        num = 0
        while True:
            try:
                pickle.load(file)
                num += 1
            except EOFError:
                break
        return num


def num_augmented_games_in_file(file):
    with (open(file, "rb")) as file:
        num = 0
        while True:
            try:
                data_dic = pickle.load(file)
                if data_dic['game_mode'][0] == PARTNER_MODE:
                    num += 6
                else:
                    num += 24
            except EOFError:
                break
        return num


def prepare_data_bidding(game_data_dic, augment_data=False):

    player_hands = game_data_dic['player_hands']
    game_mode = game_data_dic['game_mode']
    declaring_player = game_data_dic['declaring_player']

    data_list = []

    if not augment_data:
        for hand, player_pos in zip(player_hands, range(len(player_hands))):
            x, y = create_bidding_example(declaring_player, game_mode, hand, player_pos)
            data_list.append((x, y))
    elif game_mode[0] == PARTNER_MODE:
        data_list += suit_permutations_hands_partner(declaring_player, game_mode, player_hands)
    else:
        data_list += suit_permutations_hands_sw(declaring_player, game_mode, player_hands)
    return data_list


def suit_permutations_hands_partner(declaring_player, game_mode, player_hands):
    data_list = []
    # augment by getting all suit permutations via two transpositions
    # first cycle through all possible game_suits
    for new_game_suit in [BELLS, LEAVES, ACORNS]:
        new_player_hands = switch_suits_player_hands(player_hands, game_mode[1], new_game_suit)
        new_game_mode = (PARTNER_MODE, new_game_suit)
        other_suits = [s for s in [BELLS, LEAVES, ACORNS] if s != new_game_suit]
        first_suit = other_suits[0]
        # then both permutations of the remaining two suits
        for sec_suit in other_suits:
            new_player_hands = switch_suits_player_hands(new_player_hands, first_suit, sec_suit)
            # now create trainingsexamples from switched hands
            for hand, player_pos in zip(new_player_hands, range(len(player_hands))):
                x, y = create_bidding_example(declaring_player, new_game_mode, hand, player_pos)
                data_list.append((x, y))
    return data_list


def suit_permutations_hands_sw(declaring_player, game_mode, player_hands):
    data_list = []
    # augment by getting all suit permutations via three transpositions
    # first cycle through all possible game_suits
    for new_game_suit in SUITS:
        new_player_hands = switch_suits_player_hands(player_hands, game_mode[1], new_game_suit)
        new_game_mode = (PARTNER_MODE, new_game_suit)
        other_suits = [s for s in SUITS if s != new_game_suit]
        first_suit = other_suits[0]
        # then permutations of 3 remaining elements again by two permutations
        for sec_suit in other_suits:
            new_player_hands = switch_suits_player_hands(new_player_hands, sec_suit, first_suit)
            remaining_suits = [s for s in other_suits if s != first_suit]
            for third_suit in remaining_suits:
                new_player_hands = switch_suits_player_hands(new_player_hands, sec_suit, third_suit)
                # now create trainingsexamples from switched hands
                for hand, player_pos in zip(new_player_hands, range(len(player_hands))):
                    x, y = create_bidding_example(declaring_player, new_game_mode, hand, player_pos)
                    data_list.append((x, y))
    return data_list


def create_bidding_example(declaring_player, game_mode, hand, player_pos):
    x = enc.encode_one_hot_hand(hand)
    if player_pos == declaring_player:
        y = enc.encode_one_hot_game_mode(game_mode)
    else:
        y = enc.encode_one_hot_game_mode((NO_GAME, None))
    return x, y


def load_data_bidding(file, augment_data=False):
    if not augment_data:
        num_games = num_games_in_file(file)
        with open(file, 'rb') as infile:

            x_data = np.zeros(shape=(num_games * 4, 8, 32))
            y_data = np.zeros(shape=(num_games * 4, 9))

            for game_num in range(num_games):
                game_data_dic = pickle.load(infile)
                data_list = prepare_data_bidding(game_data_dic)
                for hand_num in range(len(data_list)):
                    x, y = data_list[hand_num]
                    x_data[game_num * 4 + hand_num] = x
                    y_data[game_num * 4 + hand_num] = y
    else:

        num_examples_augmented = num_augmented_games_in_file(file) * 4
        num_games = num_games_in_file(file)
        with open(file, 'rb') as infile:

            x_data = np.zeros(shape=(num_examples_augmented, 8, 32))
            y_data = np.zeros(shape=(num_examples_augmented, 9))
            next_index = 0

            for game_num in range(num_games):
                game_data_dic = pickle.load(infile)
                data_list = prepare_data_bidding(game_data_dic, augment_data=True)
                for hand_num in range(len(data_list)):
                    x, y = data_list[hand_num]
                    x_data[next_index] = x
                    y_data[next_index] = y
                    next_index += 1

    return x_data, y_data


def prepare_data_trickplay(game_data_dic, num_samples=1):

    played_cards = game_data_dic['played_cards']
    card_sequences = []
    cards_to_predict = []

    # create num_samples different sequences from one game
    seq_lenghts = random.sample(range(27), num_samples)

    for seq_len in seq_lenghts:
        seq = played_cards[:seq_len]
        seq_encoded = enc.encode_played_cards(seq, next_rel_pos=played_cards[seq_len][1])
        card_sequences.append(seq_encoded)
        next_card = played_cards[seq_len][0]
        cards_to_predict.append(enc.encode_one_hot_card(next_card))

    return card_sequences, cards_to_predict


def load_data_trickplay(file, num_samples=1):    # maybe augment data as well?

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


def prepare_data_inference(game_data_dic, num_samples):
    '''creates lists X, Y with X containing card_seq and Y containing encoded player_hands (starting player first)'''
    played_cards = game_data_dic['played_cards']
    player_hands = game_data_dic['player_hands']

    card_sequences = []
    hands_to_predict = []

    # create num_samples different sequences from one game
    seq_lenghts = random.sample(range(1, 27), num_samples)

    for seq_len in seq_lenghts:
        seq = played_cards[:seq_len]
        seq_encoded = enc.encode_played_cards(seq, next_rel_pos=played_cards[seq_len][1])
        card_sequences.append(seq_encoded)

        player_hands_to_predict = np.zeros(128)

        for index, hand in enumerate(player_hands):
            remaining_hand = [card for card in hand if card not in [c[0] for c in seq]]
            rem_hand_encoded = enc.encode_hand_inference(remaining_hand)
            player_hands_to_predict[index * 32: index * 32 + 32] = rem_hand_encoded

        hands_to_predict.append(player_hands_to_predict)

    return card_sequences, hands_to_predict


def prepare_extended_data_inference(game_data_dic, num_samples):
    """creates lists [X1, X2], Y with X1 containing card_seq, X2 containing the player hand,
     and Y containing encoded opponent_hands (starting player first)"""
    played_cards = game_data_dic['played_cards']
    player_hands = game_data_dic['player_hands']

    card_sequences = []
    aux_input_hands = []
    hands_to_predict = []

    # create num_samples different sequences from one game
    seq_lenghts = random.sample(range(1, 27), num_samples)

    for seq_len in seq_lenghts:
        seq = played_cards[:seq_len]
        seq_encoded = enc.encode_played_cards(seq, next_rel_pos=played_cards[seq_len][1])
        card_sequences.append(seq_encoded)

        next_player = played_cards[seq_len][1]
        pl_hand = player_hands[next_player]
        hand_enc = enc.encode_one_hot_hand(pl_hand)
        aux_input_hands.append(hand_enc)

        player_hands_to_predict = np.zeros(96)

        shift = 0
        for index, hand in enumerate(player_hands):
            start_ind = (index + shift) * 32
            if index == next_player:
                shift = -1
                continue
            else:
                remaining_hand = [card for card in hand if card not in [c[0] for c in seq]]
                rem_hand_encoded = enc.encode_hand_inference(remaining_hand)
                player_hands_to_predict[start_ind: start_ind + 32] = rem_hand_encoded

        hands_to_predict.append(player_hands_to_predict)

    return card_sequences, aux_input_hands, hands_to_predict


def load_extended_data_inference(file, num_samples=1):    # maybe augment data as well?

    num_games = num_games_in_file(file)

    with open(file, 'rb') as infile:

        x_card_seq = np.zeros(shape=(num_games * num_samples, 28, 36))
        x_aux_input_hands = np.zeros(shape=(num_games * num_samples, 8, 32))
        y_data = np.zeros(shape=(num_games * num_samples, 96))

        for game_num in range(num_games):
            game_data_dic = pickle.load(infile)
            card_sequences, aux_hands, hands_to_predict = prepare_extended_data_inference(game_data_dic, num_samples)
            for num in range(num_samples):
                x1 = card_sequences[num]
                x2 = aux_hands[num]
                y = hands_to_predict[num]

                x_card_seq[game_num * num_samples + num] = x1
                x_aux_input_hands[game_num * num_samples + num] = x2
                y_data[game_num * num_samples + num] = y

    return [x_card_seq, x_aux_input_hands], y_data


def load_data_inference(file, num_samples=1):    # maybe augment data as well?

    num_games = num_games_in_file(file)

    with open(file, 'rb') as infile:

        x_data = np.zeros(shape=(num_games * num_samples, 28, 36))
        y_data = np.zeros(shape=(num_games * num_samples, 128))

        for game_num in range(num_games):
            game_data_dic = pickle.load(infile)
            card_sequences, hands_to_predict = prepare_data_inference(game_data_dic, num_samples)
            for num in range(num_samples):
                x = card_sequences[num]
                y = hands_to_predict[num]
                x_data[game_num * num_samples + num] = x
                y_data[game_num * num_samples + num] = y

    return x_data, y_data

