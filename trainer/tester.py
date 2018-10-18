import keras
import numpy
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from numpy import array
import logging

features = 2
window_size = 6
predictions_quantity = 6


def predict(model, y, scalarY):
    # predictions = [[0.0, 0.0] for _ in range(predictions_quantity)]
    # ynew = numpy.append(y.copy(), predictions).reshape(-1, features)
    ynew = y.copy()
    time_steps = window_size - 1
    for i, _ in enumerate(ynew):
        if i + time_steps >= len(ynew):
            break
        # ynew[i + time_steps, 0] = y[(i + time_steps) % 12, 0]
        X = ynew[i:][:time_steps]
        X = X.reshape(-1, time_steps, features)
        prediction = model.predict(X)
        ynew[i + time_steps, 1] = prediction[0, 0]

    # logging.info('y')
    # logging.info(y)
    # logging.info('ynew')
    # logging.info(ynew)
    return ynew
