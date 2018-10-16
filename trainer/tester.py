import keras
import numpy
import sqlite3
import datetime
import time
import tensorflowjs


model = keras.models.load_model('models/model.data')
raw_data = [
#     7847,
#     6528,
#     6441,
#     5372,
#     4200,
#     3431,
#     1868,
#     5676,
#     5442,
#     8044,
#     9938,
#     10067,
#     9655,
#     7790,
#     8155,
#     7782,
#     4576,
#     6465,
#     3092,
#     6375,
#     6308,
#     9266,
#     10320,
#     11297,
#     11053,
#     9199,
#     11256,
#     7258,
#     4484,
#     6493,
#     3784,
#     8938,
#     10207,
#     11594,
#     10957,
#     12183,
#     14452,
#     7790,
#     10163,
#     8162,
#     5493,
#     7141,
#     2128,
#     9041,
#     7880,
#     11275,
#     11732,
#     14142,
#     12633,
#     10411,
#     9245,
#     7975,
#     4134,
#     7046,
#     3537,
#     8549,
#     10477,
#     10629,
#     10477,
#     10629
]
raw_data = [x / 100000.0 for x in raw_data]
count = len(raw_data)
yhat = model.predict(numpy.array(raw_data).reshape(1, count, 1))
print(yhat)
