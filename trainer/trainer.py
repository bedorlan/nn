import os
import threading
# import pymitter
import keras
import numpy
from sklearn.preprocessing import MinMaxScaler
import logging

# reshape(samples, time_steps, features)

window_size = 6
features = 2

MODEL_FILE = 'models/out.model'


class Trainer(threading.Thread):

    def init(self, trainData):
        self.trainData = trainData
        self.stopEvent = threading.Event()
        # self.on_epoch_end = pymitter.EventEmitter()

    def run(self):
        logging.info('running thread')
        data = self.getData()
        data_windows = create_windows(data, window_size)
        data_windows = numpy.array(
            data_windows).reshape(-1, window_size, features)
        model = getModel()
        X = data_windows[:, :-1]
        y = data_windows[:, -1, 1]
        #board = keras.callbacks.TensorBoard(log_dir='./logs')
        while not self.stopEvent.is_set():
            history = model.fit(X, y, epochs=1000, verbose=0)
            model.save(MODEL_FILE)
            print 'loss=', history
            # self.on_epoch_end.emit('train_result', [4, 5])
            # print 'loss=', history.history['loss'][-1]

    def stop(self):
        self.stopEvent.set()

    def getData(self):
        y = numpy.array(self.trainData)
        scalarY = MinMaxScaler(feature_range=(-1, 1))
        scalarY.fit(y)
        y = scalarY.transform(y)
        return y, scalarY


def createModel():
    model = keras.Sequential()
    model.add(keras.layers.LSTM(100, input_shape=(
        window_size-1, features), return_sequences=True))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='adam')
    model.summary()
    return model


def create_windows(y, window_size):
    return [y[i:][:window_size] for i, _ in enumerate(y)][:-window_size+1]


def getModel():
    if os.path.isfile(MODEL_FILE):
        return keras.models.load_model(MODEL_FILE)

    return createModel()
