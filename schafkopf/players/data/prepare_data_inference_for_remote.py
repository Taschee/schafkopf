import pickle
from schafkopf.players.data.load_data import load_data_inference

x_train, y_train = load_data_inference('train_data_partner.p', num_samples=1)
x_val, y_val = load_data_inference('valid_data_partner.p', num_samples=1)
x_test, y_test = load_data_inference('test_data_partner.p', num_samples=1)


with open('data_partner_inference.p', 'wb') as f:
    pickle.dump((x_train, y_train), f)
    pickle.dump((x_val, y_val), f)
    pickle.dump((x_test, y_test), f)
