import pickle
from schafkopf.players.data.load_data import load_data_inference, load_extended_data_inference

x_train, y_train = load_extended_data_inference('train_data_wenz.p', num_samples=1)
x_val, y_val = load_extended_data_inference('valid_data_wenz.p', num_samples=1)
x_test, y_test = load_extended_data_inference('test_data_wenz.p', num_samples=1)


with open('data_wenz_inference_extended.p', 'wb') as f:
    pickle.dump((x_train, y_train), f)
    pickle.dump((x_val, y_val), f)
    pickle.dump((x_test, y_test), f)
