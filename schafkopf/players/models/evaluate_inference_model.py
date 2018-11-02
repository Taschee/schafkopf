#!usr/bin/env python3

import numpy as np
import pickle
import keras

from schafkopf.game_modes import PARTNER_MODE, WENZ, SOLO
from schafkopf.players.data.load_data import load_data_inference, prepare_data_inference, num_games_in_file
import schafkopf.players.data.encodings as enc
from schafkopf.ranks import OBER, UNTER, ACE, TEN, KING, NINE, EIGHT, SEVEN
from schafkopf.suits import ACORNS, HEARTS, SUITS


filepath = '../data/test_data_solo.p'

modelpath = 'inference_model_solo_wider.hdf5'


def evaluate_model_on_testdata(model, num_games):
    with open(filepath, 'rb') as f:

        count = 0

        for num in range(num_games):

            data_dic = pickle.load(f)

            x_list, y_list = prepare_data_inference(data_dic, num_samples=26)

            for i in range(26):
                print('\n')
                x = x_list[i]
                y = y_list[i]

                predictions = model.predict(np.array([x]))[0]

                # print(predictions)
                # print(int(np.argmax(predictions)))
                # print(y)
                # print(np.where(y == 1)[0])
                if np.argmax(predictions) in np.where(y == 1)[0]:
                    count += 1

    print(count, ' / ', num_games * 27, ' Predicted best card in : ', count / (num_games * 27))


def main():
    model = keras.models.load_model(modelpath)
    num_games = num_games_in_file(filepath)
    evaluate_model_on_testdata(model, num_games)


if __name__ == '__main__':
    main()
