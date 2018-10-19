import os
import threading
import timeit
import math
import pymitter
import keras
import numpy
import sklearn
from sklearn.preprocessing import MinMaxScaler
import logging
import tester

# reshape(samples, time_steps, features)

window_size = 6
features = 2
time_steps = window_size - 1
report_time = 10

MODEL_FILE = 'models/out.model'
SCALARY_FILE = 'models/out.scalar_y'


class Trainer(threading.Thread):

    def init(self, trainData):
        self.trainData = trainData
        self.stopEvent = threading.Event()
        self.on_epoch_end = pymitter.EventEmitter()
        keras.backend.clear_session()

    def run(self):
        logging.info('running thread')
        data, scalarY = prepareData(self.trainData)
        sklearn.externals.joblib.dump(scalarY, SCALARY_FILE)

        data_windows = create_windows(data, window_size)
        data_windows = numpy.array(
            data_windows).reshape(-1, window_size, features)
        model = createModel()
        X = data_windows[:, :-1]
        y = data_windows[:, -1, 1]
        #board = keras.callbacks.TensorBoard(log_dir='./logs')
        epochs = 2
        while True:
            start = timeit.default_timer()
            history = model.fit(X, y, epochs=epochs, verbose=0)
            model.save(MODEL_FILE)
            datanew = tester.predict(model, data, scalarY)
            end = timeit.default_timer()
            if self.stopEvent.is_set():
                break

            per_epoch = (end - start) / epochs
            epochs = int(math.ceil(report_time / per_epoch))
            trainResult = [data[:, 1].tolist(), datanew[:, 1].tolist()]
            loss = history.history['loss'][-1]
            result = {"trainResult": trainResult, "loss": loss}

            self.on_epoch_end.emit('train_result', result)
            logging.info('epochs=%d, loss=%f' % (epochs, loss))

    def stop(self):
        self.stopEvent.set()


def prepareData(data, scalarY=None):
    y = numpy.array(data)
    if scalarY is None:
        scalarY = MinMaxScaler(feature_range=(-1, 1))
        scalarY.fit(y)

    y = scalarY.transform(y)
    return y, scalarY


def predict(y):
    keras.backend.clear_session()
    # assert 5 = len(y)
    y += [[0.0, 0.0]]
    scalarY = sklearn.externals.joblib.load(SCALARY_FILE)
    y, scalarY = prepareData(y)
    logging.info(y)

    model = getModel()
    ynew = tester.single_predict(model, y, scalarY)

    logging.info('prediction!')
    logging.info(ynew)

    ynew = scalarY.inverse_transform(ynew).tolist()
    return {"predictResult": ynew}


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
