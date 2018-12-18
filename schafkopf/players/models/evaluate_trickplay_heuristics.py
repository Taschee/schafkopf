import keras
import numpy as np
from schafkopf.suits import *
from schafkopf.ranks import *
import schafkopf.players.data.encodings as enc

def main():

    modelpath_partner = 'trickplay_model_partner_extended.hdf5'
    modelpath_solo = 'trickplay_model_solo_extended.hdf5'
    modelpath_wenz = 'trickplay_model_went_extended.hdf5'

    model = keras.models.load_model(modelpath_partner)

    # search
    hand_search = [(KING, HEARTS), (EIGHT, HEARTS), (TEN, ACORNS), (NINE, ACORNS),
                   (ACE, LEAVES), (EIGHT, LEAVES), (SEVEN, LEAVES), (KING, BELLS)]
    hand_partnersearch = enc.encode_one_hot_hand(hand_search)
    card_seq_partnersearch = np.zeros((28, 36))
    card_seq_partnersearch[0][34] = 1
    x = [np.array([card_seq_partnersearch]), np.array([hand_partnersearch])]

    predictions = model.predict(x)[0]

    print('Search')
    print(predictions)
    print(np.argmax(predictions))
    print(predictions[np.argmax(predictions)])
    for index in range(32):
        card_decoded = (index // 4, index % 4)
        if card_decoded not in hand_search:
            predictions[index] = 0
    print(predictions[np.argmax(predictions)] / sum(predictions))

    # offensive partner
    hand_run_away = [(OBER, LEAVES), (UNTER, HEARTS), (UNTER, BELLS), (ACE, ACORNS),
                     (EIGHT, ACORNS), (ACE, LEAVES), (SEVEN, LEAVES), (EIGHT, BELLS)]
    hand_partner_run_away = enc.encode_one_hot_hand(hand_run_away)
    card_seq_partner_run_away = np.zeros((28, 36))
    card_seq_partner_run_away[0][34] = 1
    x = [np.array([card_seq_partner_run_away]), np.array([hand_partner_run_away])]

    predictions = model.predict(x)[0]

    print('Offensive partner')
    print(predictions)
    print(np.argmax(predictions))
    print(predictions[np.argmax(predictions)])
    for index in range(32):
        card_decoded = (index // 4, index % 4)
        if card_decoded not in hand_run_away:
            predictions[index] = 0
    print(predictions[np.argmax(predictions)] / sum(predictions))

    # declaring player
    hand_partner_decl = [(OBER, ACORNS), (OBER, BELLS), (UNTER, ACORNS), (ACE, HEARTS),
                         (SEVEN, HEARTS), (EIGHT, ACORNS), (SEVEN, LEAVES), (ACE, BELLS)]
    hand_partner_decl_enc = enc.encode_one_hot_hand(hand_partner_decl)
    card_seq_partner_decl = np.zeros((28, 36))
    card_seq_partner_decl[0][32] = 1
    x = [np.array([card_seq_partner_decl]), np.array([hand_partner_decl_enc])]

    predictions = model.predict(x)[0]

    print('Offensive partner')
    print(predictions)
    print(np.argmax(predictions))
    print(predictions[np.argmax(predictions)])
    print('sum', sum(predictions))
    for index in range(32):
        card_decoded = (index // 4, index % 4)
        if card_decoded not in hand_partner_decl:
            predictions[index] = 0
    print(predictions)
    print(sum(predictions))
    print(predictions[np.argmax(predictions)] / sum(predictions))


if __name__ == '__main__':
    main()
