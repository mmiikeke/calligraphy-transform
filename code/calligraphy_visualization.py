import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    path = '../output/工.txt'
    xy = list()

    txtFile = open(path)
    for row in txtFile:
        xy.append([float(i) for i in row.split()])
    
    plt.plot([i[0] for i in xy], [i[1] for i in xy], 'ro')
    plt.show()

    