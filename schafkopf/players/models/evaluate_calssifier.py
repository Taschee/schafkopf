import keras
import numpy as np
from schafkopf.players.data.load_data import load_data_bidding
from schafkopf.players.data.encodings import decode_on_hot_hand

x_test, y_test = load_data_bidding('../data/test_data.p')
x_train, y_train = load_data_bidding('../data/train_data.p')


modelpath = "even_bigger_classifier100.hdf5"

model = keras.models.load_model(modelpath)

predictions = model.predict_classes(x_test)

num_false = 0
for pred, x, y in zip(predictions, x_test, y_test):
    y_ind = np.where(y == 1)[0][0]
    if pred != y_ind:
        num_false += 1
        print('Predicted {} instead of  {}'.format(pred, y_ind))
        print('Hand : ', decode_on_hot_hand(x))

print('Number of false predictions : ', num_false)

test_scores = model.evaluate(x_test, y_test)

val_scores = model.evaluate(x_train, y_train)
print('Total Test accuracy : ', test_scores[1])
print('Total Train accuracy : ', val_scores[1])