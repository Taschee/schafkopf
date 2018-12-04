#!usr/bin/env python3

import schafkopf.players.data.encodings as enc
import numpy as np
import pickle
import keras
import time
import matplotlib.pyplot as plt

from schafkopf.players.data.load_data import prepare_data_inference, num_games_in_file, prepare_extended_data_inference


def top_k_indices(vector, k=1):
    ind = np.argpartition(a=vector, kth=-k)[-k:]
    return ind[np.argsort(- vector[ind])]


def is_a_subset(a, b):
    return all(x in b for x in a)


def find_curr_player(seq):
    starting_player_rel = enc.decode_one_hot_player_position(seq[0][28:])
    curr_player_rel = enc.decode_one_hot_player_position(seq[0][28:])
    player = (curr_player_rel - starting_player_rel) % 4
    for i, card in enumerate(seq[1:]):
        if np.array_equal(card[:28], np.zeros(28)):
            break
        curr_player_rel = enc.decode_one_hot_player_position(card[28:])
        player = (curr_player_rel - starting_player_rel) % 4
    return player


def evaluate_model_on_testdata(model, filepath, extended_model=True, threshold=0.7):

    num_games = num_games_in_file(filepath)

    with open(filepath, 'rb') as f:

        count_correct_positives = 0
        count_false_positives = 0
        num_pred = 0

        for num in range(num_games):

            data_dic = pickle.load(f)

            if extended_model:
                card_sequences, aux_input_hands, hands_to_predict = prepare_extended_data_inference(data_dic,
                                                                                                    num_samples=26)
                y_list = hands_to_predict

                for i in range(26):

                    x = [np.array([card_sequences[i]]), np.array([aux_input_hands[i]])]
                    y = y_list[i]

                    predictions = model.predict(x)[0]
                    top_indices = top_k_indices(predictions, k=96)
                    correct_indices = np.where(y == 1)[0]

                    for index in top_indices:
                        if predictions[top_indices[index]] > threshold:
                            num_pred += 1
                            if top_indices[index] in correct_indices:
                                count_correct_positives += 1
                            else:
                                count_false_positives += 1

    return count_correct_positives / (count_correct_positives + count_false_positives), num_pred

def main():
    filepath = '../data/test_data_partner.p'

    modelpath = 'inference_model_partner_extended.hdf5'

    extended_model = True
    model = keras.models.load_model(modelpath)

    t = time.time()
    thresholds = [0.001, 0.005, 0.01, 0.015, 0.02, 0.03] + [0.05 * i for i in range(1, 20)] + [0.99]
    accuracies = []
    numbers_of_predictions = []
    for count, threshold in enumerate(thresholds):
        print(str(count / len(thresholds))[:4])
        accuracy_threshold, num_pred = evaluate_model_on_testdata(model, filepath,
                                                                  extended_model=extended_model,
                                                                  threshold=threshold)
        accuracies.append(accuracy_threshold)
        numbers_of_predictions.append(num_pred)

    print('Took {} seconds'.format(time.time() - t))
    print('Thresholds: ', thresholds)
    print('Accuracies: ', accuracies)
    print('Number of predictions: ', numbers_of_predictions)



if __name__ == '__main__':
    main()