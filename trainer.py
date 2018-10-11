import keras
import numpy
import sqlite3
import datetime
import time
import tensorflowjs


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
    8549,
    10477,
    10629,
    10477,
    10629
]
raw_data = [x / 100000.0 for x in raw_data]
count = len(raw_data)

data = numpy.array(raw_data).reshape((10, 6, 1))
x = data[:,:-1]
y = data[:,-1]

print x
print y

model = keras.models.Sequential()
# stateful=True means that the states computed for the samples in one batch will be reused as initial states for the samples in the next batch.
model.add(keras.layers.LSTM(32, input_shape=(len(x[0]), 1), dropout=0.2))
# model.add(keras.layers.LSTM(10)) # dont forget return_sequences=True in the previous layer
model.add(keras.layers.Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='adam')
model.summary()
model.fit(x, y, epochs=10000, verbose=1)

#tensorflowjs.converters.save_keras_model(model, 'models/')
model.save('models/model.data')

#test_data = [13, 14, 15, 16, 17, 18, 19, 20, 21]
#test_data = test_data[:-1]

#yhat = model.predict(numpy.array(test_data).reshape(1, 9, 1))
# print(yhat)

'''
reshape(samples, time_steps, features)
>>> np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape((2, 3, 2))
array([[[ 1,  2],
        [ 3,  4],
        [ 5,  6]],

       [[ 7,  8],
        [ 9, 10],
        [11, 12]]])
>>> a = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).reshape((3, 4, 1))
>>> a
array([[[ 1],
        [ 2],
        [ 3],
        [ 4]],

       [[ 5],
        [ 6],
        [ 7],
        [ 8]],

       [[ 9],
        [10],
        [11],
        [12]]])
>>> a[:,:-1]
array([[[ 1],
        [ 2],
        [ 3]],

       [[ 5],
        [ 6],
        [ 7]],

       [[ 9],
        [10],
        [11]]])
>>> a[:,-1]
array([[ 4],
       [ 8],
       [12]])
>>>
'''
