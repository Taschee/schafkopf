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

        count_best_card = 0
        count_two_best = 0
        count_three_best = 0
        count_four_best = 0
        count_five_best = 0

        count_best_all_hands = 0
        count_two_all_hands = 0
        count_three_all_hands = 0
        count_four_all_hands = 0
        count_five_all_hands = 0

        count_num_correct_in_top_5 = 0
        count_num_correct_in_top_5_all_hands = 0

        count_correct_positives = 0
        count_correct_positives_all_hands = 0
        count_false_positives = 0
        count_false_positives_all_hands = 0

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
                    top_indices = top_k_indices(predictions, k=5)
                    correct_indices = np.where(y == 1)[0]

                    num_correct = 0
                    if top_indices[0] in correct_indices:
                        count_best_card += 1
                        num_correct += 1
                        if predictions[top_indices[0]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[0]] > threshold:
                        count_false_positives += 1

                    if top_indices[1] in correct_indices:
                        count_two_best += 1
                        num_correct += 1
                        if predictions[top_indices[1]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[1]] > threshold:
                        count_false_positives += 1

                    if top_indices[2] in correct_indices:
                        count_three_best += 1
                        num_correct += 1
                        if predictions[top_indices[2]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[2]] > threshold:
                        count_false_positives += 1

                    if top_indices[3] in correct_indices:
                        count_four_best += 1
                        num_correct += 1
                        if predictions[top_indices[3]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[3]] > threshold:
                        count_false_positives += 1

                    if top_indices[4] in correct_indices:
                        count_five_best += 1
                        num_correct += 1
                        if predictions[top_indices[4]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[4]] > threshold:
                        count_false_positives += 1

                    count_num_correct_in_top_5 += num_correct


            else:

                x_list, y_list = prepare_data_inference(data_dic, num_samples=26)

                for i in range(26):
                    x = x_list[i]
                    y = y_list[i]
                    curr_player = find_curr_player(x)
                    curr_player_hand_indices = range(curr_player * 32, curr_player * 32 + 32)

                    predictions = model.predict(np.array([x]))[0]
                    top_indices = top_k_indices(predictions, k=5)
                    correct_indices = np.where(y == 1)[0]

                    num_correct = 0
                    num_correct_all_hands = 0

                    #  Analyze general prediction rate for all hands

                    if top_indices[0] in correct_indices:
                        count_best_all_hands += 1
                        num_correct_all_hands += 1
                        if predictions[top_indices[0]] > threshold:
                            count_correct_positives_all_hands += 1
                    elif predictions[top_indices[0]] > threshold:
                        count_false_positives_all_hands += 1

                    if top_indices[1] in correct_indices:
                        count_two_all_hands += 1
                        num_correct_all_hands += 1
                        if predictions[top_indices[1]] > threshold:
                            count_correct_positives_all_hands += 1
                    elif predictions[top_indices[1]] > threshold:
                        count_false_positives_all_hands += 1

                    if top_indices[2] in correct_indices:
                        count_three_all_hands += 1
                        num_correct_all_hands += 1
                        if predictions[top_indices[2]] > threshold:
                            count_correct_positives_all_hands += 1
                    elif predictions[top_indices[2]] > threshold:
                        count_false_positives_all_hands += 1

                    if top_indices[3] in correct_indices:
                        count_four_all_hands += 1
                        num_correct_all_hands += 1
                        if predictions[top_indices[3]] > threshold:
                            count_correct_positives_all_hands += 1
                    elif predictions[top_indices[3]] > threshold:
                        count_false_positives_all_hands += 1

                    if top_indices[4] in correct_indices:
                        count_five_all_hands += 1
                        num_correct_all_hands += 1
                        if predictions[top_indices[4]] > threshold:
                            count_correct_positives_all_hands += 1
                    elif predictions[top_indices[4]] > threshold:
                        count_false_positives_all_hands += 1

                    count_num_correct_in_top_5_all_hands += num_correct_all_hands

                    # analyze opponent hand predictions only

                    predictions = model.predict(np.array([x]))[0]
                    predictions[curr_player_hand_indices] = 0
                    top_indices = top_k_indices(predictions, k=5)

                    if top_indices[0] in correct_indices and top_indices[0] not in curr_player_hand_indices:
                        count_best_card += 1
                        num_correct += 1
                        if predictions[top_indices[0]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[0]] > threshold:
                        count_false_positives += 1

                    if top_indices[1] in correct_indices and top_indices[1] not in curr_player_hand_indices:
                        count_two_best += 1
                        num_correct += 1
                        if predictions[top_indices[1]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[1]] > threshold:
                        count_false_positives += 1

                    if top_indices[2] in correct_indices and top_indices[2] not in curr_player_hand_indices:
                        count_three_best += 1
                        num_correct += 1
                        if predictions[top_indices[2]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[2]] > threshold:
                        count_false_positives += 1

                    if top_indices[3] in correct_indices and top_indices[3] not in curr_player_hand_indices:
                        count_four_best += 1
                        num_correct += 1
                        if predictions[top_indices[3]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[3]] > threshold:
                        count_false_positives += 1

                    if top_indices[4] in correct_indices and top_indices[4] not in curr_player_hand_indices:
                        count_five_best += 1
                        num_correct += 1
                        if predictions[top_indices[4]] > threshold:
                            count_correct_positives += 1
                    elif predictions[top_indices[4]] > threshold:
                        count_false_positives += 1

                    count_num_correct_in_top_5 += num_correct

    if not extended_model:
        print('Analysis all hands : ')
        print(count_best_all_hands, ' / ', num_games * 26, ' Predicted best card in : ',
              count_best_all_hands / (num_games * 26))
        print(count_two_all_hands, ' / ', num_games * 26, ' Predicted sec card in : ',
              count_two_all_hands / (num_games * 26))
        print(count_three_all_hands, ' / ', num_games * 26, ' Predicted third card in : ',
              count_three_all_hands / (num_games * 26))
        print(count_four_all_hands, ' / ', num_games * 26, ' Predicted fourth card in : ',
              count_four_all_hands / (num_games * 26))
        print(count_five_all_hands, ' / ', num_games * 26, ' Predicted fifth card in : ',
              count_five_all_hands / (num_games * 26))
        print('Average number of correct predictions: ', count_num_correct_in_top_5_all_hands / (num_games * 26))
        print('Bigger then threshold {} : {} / {} correct, {}'.format(threshold,
                                                                      count_correct_positives_all_hands,
                                                                      count_correct_positives_all_hands + count_false_positives_all_hands,
                                                                      count_correct_positives_all_hands / (
                                                                          count_correct_positives_all_hands + count_false_positives_all_hands)))

    print('Analysis only opponent hands : ')
    print(count_best_card, ' / ', num_games * 26, ' Predicted best card in : ', count_best_card / (num_games * 26))
    print(count_two_best, ' / ', num_games * 26, ' Predicted sec card in : ', count_two_best / (num_games * 26))
    print(count_three_best, ' / ', num_games * 26, ' Predicted third card in : ', count_three_best / (num_games * 26))
    print(count_four_best, ' / ', num_games * 26, ' Predicted fourth card in : ', count_four_best / (num_games * 26))
    print(count_five_best, ' / ', num_games * 26, ' Predicted fifth card in : ', count_five_best / (num_games * 26))
    print('Average number of correct predictions: ', count_num_correct_in_top_5 / (num_games * 26))
    print('Bigger then threshold {} : {} / {} correct, {}'.format(threshold,
                                                                  count_correct_positives,
                                                                  count_correct_positives + count_false_positives,
                                                                  count_correct_positives / (
                                                                          count_correct_positives + count_false_positives)))

    return count_correct_positives / (count_correct_positives + count_false_positives)


def main():
    filepath = '../data/test_data_solo.p'

    modelpath = 'inference_model_solo_extended.hdf5'

    extended_model = True
    model = keras.models.load_model(modelpath)

    t = time.time()
    thresholds = [0.001, 0.005, 0.01, 0.015, 0.02, 0.03] + [0.05 * i for i in range(1, 20)] + [0.99]
    accuracies = []
    for threshold in thresholds:
        accuracy_threshold = evaluate_model_on_testdata(model, filepath,
                                                        extended_model=extended_model,
                                                        threshold=threshold)
        accuracies.append(accuracy_threshold)

    print('Took {} seconds'.format(time.time() - t))
    print('Thresholds: ', thresholds)
    print('Accuracies: ', accuracies)


if __name__ == '__main__':
    main()
