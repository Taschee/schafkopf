#!usr/bin/env python3

import numpy as np
import pickle
import keras
import time

from schafkopf.players.data.load_data import prepare_data_inference, num_games_in_file

filepath = '../data/test_data_solo.p'

modelpath = 'inference_model_solo_wider.hdf5'


def top_k_indices(vector, k=1):
    ind = np.argpartition(a=vector, kth=-k)[-k:]
    return ind[np.argsort(- vector[ind])]


def is_a_subset(a, b):
    return all(x in b for x in a)


def evaluate_model_on_testdata(model, num_games):
    with open(filepath, 'rb') as f:

        count_best_card = 0
        count_two_best = 0
        count_three_best = 0
        count_four_best = 0
        count_five_best = 0

        count_num_correct_in_top_5 = 0

        for num in range(num_games):

            data_dic = pickle.load(f)

            x_list, y_list = prepare_data_inference(data_dic, num_samples=26)

            for i in range(26):
                x = x_list[i]
                y = y_list[i]

                predictions = model.predict(np.array([x]))[0]
                top_indices = top_k_indices(predictions, k=5)
                correct_indices = np.where(y == 1)[0]

                num_correct = 0
                if top_indices[0] in correct_indices:
                    count_best_card += 1
                    num_correct += 1
                if top_indices[1] in correct_indices:
                    count_two_best += 1
                    num_correct += 1
                if top_indices[2] in correct_indices:
                    count_three_best += 1
                    num_correct += 1
                if top_indices[3] in correct_indices:
                    count_four_best += 1
                    num_correct += 1
                if top_indices[4] in correct_indices:
                    count_five_best += 1
                    num_correct += 1

                count_num_correct_in_top_5 += num_correct

    print(count_best_card, ' / ', num_games * 26, ' Predicted best card in : ', count_best_card / (num_games * 26))
    print(count_two_best, ' / ', num_games * 26, ' Predicted sec card in : ', count_two_best / (num_games * 26))
    print(count_three_best, ' / ', num_games * 26, ' Predicted third card in : ', count_three_best / (num_games * 26))
    print(count_four_best, ' / ', num_games * 26, ' Predicted fourth card in : ', count_four_best / (num_games * 26))
    print(count_five_best, ' / ', num_games * 26, ' Predicted fifth card in : ', count_five_best / (num_games * 26))
    print('Average number of correct predictions: ', count_num_correct_in_top_5 / (num_games * 26))


def main():
    model = keras.models.load_model(modelpath)
    num_games = num_games_in_file(filepath)
    t = time.time()
    evaluate_model_on_testdata(model, num_games)
    print('Took {} seconds'.format(time.time() - t))

if __name__ == '__main__':
    main()
