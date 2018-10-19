import keras
import numpy
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from numpy import array
import logging

features = 2
window_size = 6
predictions_quantity = 6
time_steps = window_size - 1


def single_predict(model, y, scalarY, i=0):
    ynew = y.copy()
    X = ynew[i:][:time_steps]
    X = X.reshape(-1, time_steps, features)

    prediction = model.predict(X)
    ynew[i + time_steps, 1] = prediction[0, 0]
    return ynew


def predict(model, y, scalarY):
    # predictions = [[0.0, 0.0] for _ in range(predictions_quantity)]
    # ynew = numpy.append(y.copy(), predictions).reshape(-1, features)
    ynew = y.copy()
    for i, _ in enumerate(ynew):
        if i + time_steps >= len(ynew):
            break
        ynew = single_predict(model, ynew, scalarY, i)

    # logging.info('y')
    # logging.info(y)
    # logging.info('ynew')
    # logging.info(ynew)
    return ynew
