import os
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from data import getData

X, y, scalarX, scalarY = getData()
print X, y

MODEL_FILE = 'models/out.model'

def getModel():
    if os.path.isfile(MODEL_FILE):
        return keras.models.load_model(MODEL_FILE)

    return createModel()

def createModel():
    model = Sequential()
    model.add(Dense(1000, input_dim=1, activation='relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='adam')
    model.summary()
    return model

model = getModel()
#board = keras.callbacks.TensorBoard(log_dir='./logs')
while True:
    history = model.fit(X, y, epochs=1000, validation_split=0.05, verbose=0)
    model.save(MODEL_FILE)
    print 'loss=', history.history['loss'][-1]
