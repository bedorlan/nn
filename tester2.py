import keras
import numpy
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from numpy import array
import matplotlib.pyplot as plt
from data import getData

X, y, scalarX, scalarY = getData()

MODEL_FILE = 'models/out.model'
model = keras.models.load_model(MODEL_FILE)
model.summary()

# new instance where we do not know the answer
# make a prediction
ynew = model.predict(X)
# xnew = array([58, 59, 60]).reshape(-1, 1)
# xnew = scalarX.transform(xnew)
# ynew = model.predict(xnew)
# print ynew

plt.plot(y)
plt.plot(ynew)
plt.show()
