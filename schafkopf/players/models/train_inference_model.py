import pickle
import argparse
import numpy as np
import keras
import tensorflow as tf
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, LSTM, Dropout, Input, Flatten
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, TerminateOnNaN


def load_data(file):
    with open(file, 'rb') as f:
        x_train, y_train = pickle.load(f)
        x_val, y_val = pickle.load(f)
        x_test, y_test = pickle.load(f)
    return x_train, y_train, x_val, y_val, x_test, y_test


def top_k_indices(vector, k=1):
    ind = np.argpartition(a=vector[0], kth=-k)[-k:]
    return ind[np.argsort(- vector[ind])]


def inference_metric(y_true, y_pred):
    sess = tf.Session()
    with sess.as_default():
        sess.run(tf.global_variables_initializer())
        y_pred = y_pred.eval()
        top_indices = top_k_indices(y_pred, k=5)
    correct_indices = np.where(y_true == 1)[0]
    num_correct_pred = len(set(top_indices) & set(correct_indices))
    return K.constant(num_correct_pred)


def lstm_model():
    model = Sequential()
    model.add(LSTM(250, input_shape=(28, 36)))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])
    return model


def wider_lstm_model():
    model = Sequential()
    model.add(LSTM(500, input_shape=(28, 36)))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])
    return model


def deeper_lstm_model():
    model = Sequential()
    model.add(LSTM(250, input_shape=(28, 36), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(250))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])
    return model


def soph_model():
    seq_input = Input(shape=(28, 36),  name='seq_input')
    seq_lstm = LSTM(250)(seq_input)
    hand_input = Input(shape=(8, 32), name='hand_imput')
    flatten = Flatten()(hand_input)
    concat_layer = keras.layers.concatenate([seq_lstm, flatten])
    hidden = Dense(250, activation='elu', kernel_initializer='he_uniform')(concat_layer)
    out_layer = Dense(96, activation='sigmoid')(hidden)
    model = Model(inputs=[seq_input, hand_input], outputs=out_layer)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])
    return model


def train(model, x_train, y_train, x_val, y_val, epochs, modelname='model.hdf5'):

    checkpoint = ModelCheckpoint(modelname, monitor='mse', verbose=1, save_best_only=True, mode='max')
    tensorboard = TensorBoard(log_dir='./logs')
    callback_list = [checkpoint, TerminateOnNaN(), tensorboard]

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
    parser.add_argument('--wider_lstm', help='use two lstm blocks of 250 cells', action='store_true')
    parser.add_argument('--deeper_lstm', help='use two lstm blocks of 250 cells', action='store_true')
    parser.add_argument('--soph_model',
                        help='use more sophisticated model with player hand as extra input, needs different data',
                        action='store_true')
    args = parser.parse_args()

    x_train, y_train, x_val, y_val, _, _ = load_data(args.data)

    if args.soph_model:
        assert type(x_train) == list \
               and x_train[0].shape[1:] == (28, 36) \
               and x_train[1].shape[1:] == (8, 32), 'Wrong trainings data format'
        assert y_train.shape[1:] == (96, ), 'Wrong trainings data format'
    else:
        assert x_train.shape[1:] == (28, 36), 'Wrong trainings data format'
        assert y_train.shape[1:] == (128, ), 'Wrong trainings data format'

    if args.epochs:
        num_epochs = args.epochs
    else:
        num_epochs = 20

    if args.soph_model:
        model = soph_model()

    elif args.deeper_lstm:
        model = deeper_lstm_model()
    elif args.wider_lstm:
        model = wider_lstm_model()
    else:
        model = lstm_model()

    if args.modelname:
        train(model, x_train, y_train, x_val, y_val,  epochs=num_epochs, modelname=args.modelname)
    else:
        train(model, x_train, y_train, x_val, y_val, epochs=num_epochs, modelname='model.hdf5')


if __name__ == '__main__':
    main()
