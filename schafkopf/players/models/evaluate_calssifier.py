import keras
import numpy as np
from schafkopf.players.data.load_data import load_data_bidding
from schafkopf.players.data.encodings import decode_on_hot_hand
import matplotlib.pyplot as plt

x_test, y_test = load_data_bidding('../data/test_data.p')
x_train, y_train = load_data_bidding('../data/train_data.p')

modelpath = "bigger_classifier50.hdf5"

model = keras.models.load_model(modelpath)

predictions = model.predict_classes(x_test)

false_pred_list = []

pairs = [(i, j) for i in range(9) for j in range(9)]
false_counts = {pair: 0 for pair in pairs}

for pred, x, y in zip(predictions, x_test, y_test):
    y_ind = np.where(y == 1)[0][0]
    if pred != y_ind:
        false_pred_list.append((pred, y_ind))
        print('Predicted {} instead of  {}'.format(pred, y_ind))
        print('Hand : ', decode_on_hot_hand(x))

num_false = len(false_pred_list)
print('Number of false predictions : ', num_false)

for pair in false_pred_list:
    false_counts[pair] += 1

fig, ax = plt.subplots(1, 1)
tick_labels = ['No game', 'Partner, bells', 'Partner, Leaves', 'Partner, Acorns',
               'Wenz', 'Solo, Bells', 'Solo, Hearts', 'Solo, Leaves', 'Solo, Acorns']

for y_pred, y_true in pairs:
    plt.scatter(y_pred, y_true, s=3*false_counts[(y_pred, y_true)], c='blue', alpha=0.6)

ax.set_xticks(np.arange(0, 9, 1))
ax.set_xticklabels(tick_labels, rotation='vertical', fontsize=11)
ax.set_yticks(np.arange(0, 9, 1))
ax.set_yticklabels(tick_labels, rotation='horizontal', fontsize=11)
ax.set_xlabel('Bidding network', fontsize=13)
ax.set_ylabel('Human player', fontsize=13)
ax.axis('equal')
plt.tight_layout()
plt.show()

test_scores = model.evaluate(x_test, y_test)

val_scores = model.evaluate(x_train, y_train)
print('Total Test accuracy : ', test_scores[1])
print('Total Train accuracy : ', val_scores[1])





