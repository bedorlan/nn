import os
import keras
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from numpy import array

# generate regression dataset
raw_data = [
    7847,
    6528,
    6441,
    5372,
    4200,
    3431,
    1868,
    5676,
    5442,
    8044,
    9938,
    10067,
    9655,
    7790,
    8155,
    7782,
    4576,
    6465,
    3092,
    6375,
    6308,
    9266,
    10320,
    11297,
    11053,
    9199,
    11256,
    7258,
    4484,
    6493,
    3784,
    8938,
    10207,
    11594,
    10957,
    12183,
    14452,
    7790,
    10163,
    8162,
    5493,
    7141,
    2128,
    9041,
    7880,
    11275,
    11732,
    14142,
    12633,
    10411,
    9245,
    7975,
    4134,
    7046,
    3537,
    # 8549,
    # 10477,
    # 10629
]
# raw_data = [1, 4, 2, 5, 3]
count = len(raw_data)

X = array([i for i,x in enumerate(raw_data)])
y = array(raw_data).reshape(-1, 1)
scalarX, scalarY = MinMaxScaler(), MinMaxScaler()
scalarX.fit(numpy.append(X, 100).reshape(-1, 1))
scalarY.fit(y)
X = scalarX.transform(X.reshape(-1, 1))
y = scalarY.transform(y)
print X, y
# define and fit the final model

MODEL_FILE = 'models/out.model'

def getModel():
    if os.path.isfile(MODEL_FILE):
        return keras.models.load_model(MODEL_FILE)

    return createModel()

def createModel():
    model = Sequential()
    model.add(Dense(1000, input_dim=1, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='adam')
    model.summary()
    return model

model = getModel()
while True:
    history = model.fit(X, y, epochs=1000, verbose=0)
    model.save(MODEL_FILE)
    print 'loss=', history.history['loss'][-1]
