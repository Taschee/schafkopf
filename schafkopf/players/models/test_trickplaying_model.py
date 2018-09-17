import numpy as np
import pickle
import keras
from schafkopf.players.data.load_data import load_data_trickplay, prepare_data_trickplay, num_games_in_file
import schafkopf.players.data.encodings as enc


filepath = '../data/test_data_partner.p'

modelpath = 'partner_model_small_1.hdf5'

model = keras.models.load_model(modelpath)

num_games = num_games_in_file(filepath)

with open(filepath, 'rb') as f:

    count = 0

    for num in range(num_games):

        data_dic = pickle.load(f)

        x_list, y_list = prepare_data_trickplay(data_dic, num_samples=1)
        x = x_list[0]
        y = y_list[0]
        predictions = model.predict(np.array([x]))[0]

        next_card = enc.decode_one_hot_card(y)
        for card, pl in data_dic['played_cards']:
            if card == next_card:
                player = pl
                break

        player_hand = data_dic['player_hands'][player]

        for crd, pl in data_dic['played_cards']:
            if crd == next_card:
                break
            elif pl == player:
                player_hand = [c for c in player_hand if c != crd]

        deck = [(i // 4, i % 4) for i in range(32)]
        pred_actual = predictions[:]
        for c in deck:
            if c not in player_hand:
                index = c[0] * 4 + c[1]
                pred_actual[index] = 0

        if np.argmax(y) == np.argmax(pred_actual):
            count += 1

print(count, ' / ', num_games, ' Accuracy : ', count/num_games)

# plan:
# get player hands as well. set all entrys for cards not in hand to zero (and renormalize).
# check prediction then!
# Well: could be improved by only using possible cards to play

