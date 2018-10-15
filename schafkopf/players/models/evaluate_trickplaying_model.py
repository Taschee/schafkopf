#!usr/bin/env python3

import numpy as np
import pickle
import keras

from schafkopf.game_modes import PARTNER_MODE, WENZ, SOLO
from schafkopf.players.data.load_data import load_data_trickplay, prepare_data_trickplay, num_games_in_file
import schafkopf.players.data.encodings as enc
from schafkopf.ranks import OBER, UNTER, ACE, TEN, KING, NINE, EIGHT, SEVEN
from schafkopf.suits import ACORNS, HEARTS, SUITS
from schafkopf.trick import Trick


# make this more reproducible ->
game_mode = (PARTNER_MODE, ACORNS)

filepath = '../data/test_data_wenz.p'

modelpath = 'wenz_model_wider_data_10.hdf5'


def suit_in_hand(suit, hand, trumpcards):
    suit_cards = [card for card in hand if card[1] == suit and card not in trumpcards]
    if len(suit_cards) > 0:
        return suit_cards
    else:
        return hand


def possible_cards(game_mode, current_trick, hand, previously_ran_away):
    assert game_mode in [(PARTNER_MODE, ACORNS), (WENZ, None), (SOLO, HEARTS)]
    if game_mode == (PARTNER_MODE, ACORNS) or game_mode == (SOLO, HEARTS):
        trumpcards = [(OBER, suit) for suit in SUITS] + [(UNTER, suit) for suit in SUITS] + \
                     [(ACE, HEARTS), (TEN, HEARTS), (KING, HEARTS),
                      (NINE, HEARTS), (EIGHT, HEARTS), (SEVEN, HEARTS)]
    else:
        trumpcards = [(UNTER, suit) for suit in SUITS]
    if current_trick.num_cards == 0:
        # " Check in case of PARTNER MODE if running away is possible"
        if game_mode[0] == PARTNER_MODE and (ACE, game_mode[1]) in hand:
            if len(suit_in_hand(suit=game_mode[1], hand=hand, trumpcards=trumpcards)) < 4:
                forbidden_cards = [card for card in hand if card not in trumpcards
                                   and card[1] == game_mode[1] and card[0] != 7]
                poss_cards = [card for card in hand if card not in forbidden_cards]
            else:
                poss_cards = hand
        else:
            poss_cards = hand

    else:
        first_card = current_trick.cards[current_trick.leading_player_index]

        if first_card in trumpcards:
            players_trumpcards = [trump for trump in trumpcards if trump in hand]
            if len(players_trumpcards) > 0:
                poss_cards = players_trumpcards
            else:
                poss_cards = hand
        elif game_mode[0] == PARTNER_MODE and first_card[1] == game_mode[1] \
                and (7, game_mode[1]) in hand:
            if not previously_ran_away:
                poss_cards = [(7, game_mode[1])]
            else:
                suit = first_card[1]
                poss_cards = suit_in_hand(suit, hand, trumpcards)
        else:
            suit = first_card[1]
            poss_cards = suit_in_hand(suit, hand, trumpcards)

    return poss_cards[:]


def get_possible_cards(game_mode, card_sequence, player_hand):
    num_cards_curr_trick = len(card_sequence) % 4
    if len(card_sequence) == 0:
        return player_hand
    else:
        first_card = card_sequence[-num_cards_curr_trick][0]
        leading_player = card_sequence[-num_cards_curr_trick][1]
        curr_trick = Trick(leading_player_index=leading_player)
        curr_trick.num_cards = num_cards_curr_trick
        curr_trick.cards[leading_player] = first_card
        previously_ran_away = False
        if game_mode == (PARTNER_MODE, ACORNS):
            num_tricks_before = len(card_sequence) // 4
            for card_index in range(0, num_tricks_before, 4):
                # check if ACORNS was played in that trick
                first_card = card_sequence[card_index][0]
                if first_card[1] == ACORNS and first_card[0] not in [UNTER, OBER]:
                    # if yes, check if ACE was played
                    cards_in_trick = [c[0] for c in card_sequence[card_index: card_index + 4]]
                    if (ACE, ACORNS) not in cards_in_trick:
                        previously_ran_away = True
        return possible_cards(game_mode, curr_trick, player_hand, previously_ran_away)


def evaluate_model_on_testdata(model, num_games):
    with open(filepath, 'rb') as f:

        count = 0

        for num in range(num_games):

            data_dic = pickle.load(f)

            x_list, y_list = prepare_data_trickplay(data_dic, num_samples=1)
            x = x_list[0]
            y = y_list[0]

            predictions = model.predict(np.array([x]))[0]

            card_to_predict = enc.decode_one_hot_card(y)
            card_sequence = []

            # find current player
            for card, pl in data_dic['played_cards']:
                if card == card_to_predict:
                    player = pl
                    break
                else:
                    card_sequence.append((card, pl))

            player_hand = data_dic['player_hands'][player]
            assert card_to_predict in player_hand, 'Card to predict was not in player hand'

            for crd, pl in data_dic['played_cards']:
                if crd == card_to_predict:
                    break
                elif pl == player:
                    player_hand = [c for c in player_hand if c != crd]


            options = get_possible_cards(game_mode, card_sequence, player_hand)

            deck = [(i // 4, i % 4) for i in range(32)]
            pred_actual = predictions[:]
            for c in deck:
                if c not in options:
                    index = c[0] * 4 + c[1]
                    pred_actual[index] = 0

            if np.argmax(y) == np.argmax(pred_actual):
                count += 1
    print(count, ' / ', num_games, ' Accuracy : ', count / num_games)


def main():
    model = keras.models.load_model(modelpath)
    num_games = num_games_in_file(filepath)
    evaluate_model_on_testdata(model, num_games)


if __name__ == '__main__':
    main()

