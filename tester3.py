import keras
import numpy
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from numpy import array
import matplotlib.pyplot as plt
from data3 import getData

MODEL_FILE = 'models/out.model'
model = keras.models.load_model(MODEL_FILE)
model.summary()

y, scalarY = getData()
features = 2
window_size = 6
time_steps = window_size - 1

predictions = [[0.0, 0.0] for _ in range(12)]
ynew = numpy.append(y.copy(), predictions).reshape(-1, features) # aqui almacenamos la ultima prediccion
for i,_ in enumerate(ynew):
    if i + time_steps >= len(ynew):
        break
    ynew[i + time_steps, 0] = y[(i + time_steps) % 12, 0]
    X = ynew[i:][:time_steps]
    X = X.reshape(-1, time_steps, features)
    prediction = model.predict(X)
    ynew[i + time_steps, 1] = prediction[0, 0]

# __import__('ipdb').set_trace()
plt.plot(y[:,1])
plt.plot(ynew[:,1])
plt.show()
