import pickle
from schafkopf.players.data.load_data import load_data_trickplay

x_train, y_train = load_data_trickplay('train_data_partner.p', num_samples=2)
x_val, y_val = load_data_trickplay('valid_data_partner.p', num_samples=2)
x_test, y_test = load_data_trickplay('test_data_partner.p', num_samples=2)

with open('data_partner_2.p', 'wb') as f:
    pickle.dump((x_train, y_train), f)
    pickle.dump((x_val, y_val), f)
    pickle.dump((x_test, y_test), f)
