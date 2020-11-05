"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
if __name__ == "__main__":
    fig = plt.figure(figsize=(20,10))
    ims = []
    for i in range(1,10):
        im = plt.plot(np.linspace(0, i,10), np.linspace(0, np.random.randint(i),10))
        ims.append(im)
    ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)
    ani.save("test.gif",writer='pillow')
"""
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
ims=[]

for iternum in range(4):
    ttl = plt.text(0.5, 1.01, iternum, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
    txt = plt.text(iternum,iternum,iternum)
    ims.append([plt.scatter(np.random.randint(0,10,5), np.random.randint(0,20,5),marker='+'    ), ttl, txt])
    #plt.cla()


ani = animation.ArtistAnimation(fig, ims, interval=500, blit=False,
                              repeat_delay=2000)
plt.show()
"""
import os, sys
sys.path.append('..')

import matplotlib.pyplot as plt
from calligraphy_transform import calligraphy_transform
from utils.tools import save_file

if __name__ == '__main__':
    path = '../../data/6axis/char00126_stroke.txt'
    #output_path1 = '../o/3d.txt'
    #output_path2 = '../o/3d_1.txt'
    #output_path3 = '../o/3d_2.txt'
    #output_path4 = '../o/6dcmd.txt'

    calligraphy_tool = calligraphy_transform()
    z0_point = 3.5 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322] -2.85887236e-03 [-130.099, 459.278,182.715,175.55,-7.84099,70.2961]
    data_6d, data_cmd = calligraphy_tool.read_file(path, is_6dcmd=True)
    strokes = calligraphy_tool.find_stroke(data_cmd)
    #colors = ['b','c','r','g','m','y','k']
    colors = ['r','y','g','b','c','m','k']

    for i in range(len(strokes)-1):
        data_6d_1, data_6d_2, data_cmd_1, data_cmd_2 = calligraphy_tool.data_6d_cmd_split(data_6d, data_cmd, i, i+1)
        calligraphy_tool.visualize_line_6d(data_6d_2, data_cmd_2, z0_point, with_thickness=True, color=colors[i%len(colors)], plot=False)

    plt.show()