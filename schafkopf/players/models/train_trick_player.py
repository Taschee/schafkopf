from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from schafkopf.players.data.load_data import load_data_trickplay


x_train, y_train = load_data_trickplay('../data/train_data_partner.p')
x_val, y_val = load_data_trickplay('../data/valid_data_partner.p')


model = Sequential()
model.add(LSTM(256, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y_train.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

filepath="partner1.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(x_train, y_train, epochs=30, validation_data=(x_val, y_val) ,batch_size=128, callbacks=callbacks_list)
