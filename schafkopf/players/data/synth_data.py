from schafkopf.suits import SUITS
from schafkopf.ranks import OBER, UNTER
from schafkopf.game_modes import SOLO
from schafkopf.players.data.load_data import num_games_in_file
import pickle
import random

# synthetical data from SOLOS: expected value is always the best OBER/UNTER which is still in the game

filename = 'train_data.p'

num = num_games_in_file(filename)

with open(filename, 'rb') as f:

    for game_num in range(num):
        data_dic = pickle.load(f)

        if data_dic['game_mode'][0] == SOLO:

            off_player = data_dic['declaring_player']
            played_cards = [data[0] for data in data_dic['played_cards']]
            high_trumpcards = [(OBER, suit) for suit in SUITS] + [(UNTER, suit) for suit in SUITS]

            while True:
                seq_len = random.choice(27)
                card_sequence = played_cards[:seq_len]
                best_trumpcard = None

                for index in range(8):
                    best_trumpcard = high_trumpcards[index]
                    if best_trumpcard not in card_sequence:
                        break

                if best_trumpcard is not None:
                    break







