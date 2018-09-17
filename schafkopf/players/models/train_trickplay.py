import pickle
import argparse
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, TerminateOnNaN


def load_data(file):
    with open(file, 'rb') as f:
        x_train, y_train = pickle.load(f)
        x_val, y_val = pickle.load(f)
        x_test, y_test = pickle.load(f)
    return x_train, y_train, x_val, y_val, x_test, y_test


def lstm_model():
    model = Sequential()
    model.add(LSTM(256, input_shape=(28, 36)))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def bigger_lstm_model():
    model = Sequential()
    model.add(LSTM(256, input_shape=(28, 36)))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def train(model, x_train, y_train, x_val, y_val, epochs, modelname='model.hdf5'):

    checkpoint = ModelCheckpoint(modelname, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    early_stopping = EarlyStopping(patience=3)
    tensorboard = TensorBoard(log_dir='./logs')
    callback_list = [checkpoint, TerminateOnNaN(), early_stopping, tensorboard]

    model.fit(x_train, y_train,
              epochs=epochs,
              validation_data=(x_val, y_val),
              batch_size=128,
              callbacks=callback_list)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='pickle file with the trainings data')
    parser.add_argument('--modelname', help='name of the model to be trained')
    parser.add_argument('--epochs', help='number of training epochs', type=int)
    parser.add_argument('--bigger_lstm', help='use two lstm blocks', action='store_true')
    args = parser.parse_args()

    x_train, y_train, x_val, y_val, _, _ = load_data(args.data)

    if args.epochs:
        num_epochs = args.epochs
    else:
        num_epochs = 10

    if args.bigger_lstm:
        model = bigger_lstm_model()
    else:
        model = lstm_model()

    if args.modelname:
        train(model, x_train, y_train, x_val, y_val,  epochs=num_epochs, modelname=args.modelname)
    else:
        train(model, x_train, y_train, x_val, y_val, epochs=num_epochs)


if __name__ == '__main__':
    main()
