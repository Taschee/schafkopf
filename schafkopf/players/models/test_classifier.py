import keras
import numpy as np
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, UNTER, OBER, KING, ACE
from schafkopf.suits import BELLS, ACORNS, HEARTS, LEAVES
import schafkopf.players.data.encodings as enc


filepath = "bigger_classifier50.hdf5"

model = keras.models.load_model(filepath)

hand_wenz = enc.encode_one_hot_hand([(UNTER, ACORNS), (UNTER, HEARTS), (ACE, BELLS), (ACE, LEAVES),
                                     (EIGHT, LEAVES), (ACE, ACORNS), (EIGHT, BELLS), (SEVEN, BELLS)])

hand_solo_leaves = enc.encode_one_hot_hand([(OBER, ACORNS), (OBER, HEARTS), (OBER, BELLS), (UNTER, ACORNS),
                                            (UNTER, BELLS), (TEN, LEAVES), (NINE, LEAVES), (SEVEN, HEARTS)])

hand_partner_leaves = enc.encode_one_hot_hand([(OBER, ACORNS), (OBER, HEARTS), (UNTER, BELLS), (ACE, HEARTS),
                                              (NINE, HEARTS), (EIGHT, BELLS), (TEN, LEAVES), (ACE, ACORNS)])

hand_no_game = enc.encode_one_hot_hand([(OBER, ACORNS), (KING, HEARTS), (ACE, BELLS), (TEN, BELLS),
                                        (EIGHT, BELLS), (SEVEN, BELLS), (KING, ACORNS), (NINE, ACORNS)])

hands = np.array([hand_wenz, hand_solo_leaves, hand_partner_leaves, hand_no_game])

print(model.predict(np.array([hand_wenz])))
print(model.predict(np.array([hand_solo_leaves])))
print(model.predict(np.array([hand_partner_leaves])))
print(model.predict(np.array([hand_no_game])))

print(model.predict_classes(hands))
