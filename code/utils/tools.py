import os
import math
import pandas as pd

def save_file(savepath, data, sep = ' ', index = False, header = False, warning = True):
    df = pd.DataFrame(data)
    dirpath = os.path.dirname(savepath)

    if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

    if os.path.isfile(savepath):
        print('Warning: File already exists! ' + savepath)

    print('Save file: ' + savepath)
    df.to_csv(savepath, index=index, header=header, sep=' ')

def sigmoid(x):
    return 1/(1+math.exp(-x))

def angle2deg(angle):
    return angle * math.pi / 180 