import os
import keras
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers import TimeDistributed
from keras.layers import Dropout
from data3 import getData

# reshape(samples, time_steps, features)


def create_windows(y, window_size):
    return [y[i:][:window_size] for i, _ in enumerate(y)][:-window_size+1]


window_size = 6
features = 2
data, scalar_data = getData()
data_windows = create_windows(data, window_size)
data_windows = numpy.array(data_windows).reshape(-1, window_size, features)
print data_windows

MODEL_FILE = 'models/out.model'


def getModel():
    if os.path.isfile(MODEL_FILE):
        return keras.models.load_model(MODEL_FILE)

    return createModel()


def createModel():
    model = Sequential()
    model.add(LSTM(100, input_shape=(
        window_size-1, features), return_sequences=True))
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='adam')
    model.summary()
    return model


model = getModel()
X = data_windows[:, :-1]
y = data_windows[:, -1, 1]
#board = keras.callbacks.TensorBoard(log_dir='./logs')
while True:
    history = model.fit(X, y, epochs=1000, verbose=0)
    model.save(MODEL_FILE)
    print 'loss=', history.history['loss'][-1]
