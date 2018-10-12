import numpy
from sklearn.preprocessing import MinMaxScaler
from numpy import array

raw_data = [
    [1, 7847],
    [2, 6528],
    [3, 6441],
    [4, 5372],
    [5, 4200],
    [6, 3431],
    [7, 1868],
    [8, 5676],
    [9, 5442],
    [10, 8044],
    [11, 9938],
    [12, 10067],
    [1, 9655],
    [2, 7790],
    [3, 8155],
    [4, 7782],
    [5, 4576],
    [6, 6465],
    [7, 3092],
    [8, 6375],
    [9, 6308],
    [10, 9266],
    [11, 10320],
    [12, 11297],
    [1, 11053],
    [2, 9199],
    [3, 11256],
    [4, 7258],
    [5, 4484],
    [6, 6493],
    [7, 3784],
    [8, 8938],
    [9, 10207],
    [10, 11594],
    [11, 10957],
    [12, 12183],
    [1, 14452],
    [2, 7790],
    [3, 10163],
    [4, 8162],
    [5, 5493],
    [6, 7141],
    [7, 2128],
    [8, 9041],
    [9, 7880],
    [10, 11275],
    [11, 11732],
    [12, 14142],
    [1, 12633],
    [2, 10411],
    [3, 9245],
    [4, 7975],
    [5, 4134],
    [6, 7046],
    [7, 3537],
    [8, 8549],
    [9, 10477],
    [10, 10629],
]

def getData():
    y = array(raw_data)
    scalarY = MinMaxScaler(feature_range=(-1, 1))
    scalarY.fit(y)
    y = scalarY.transform(y)

    return y, scalarY
