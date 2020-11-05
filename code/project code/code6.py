import os, sys
sys.path.append('..')

import matplotlib.pyplot as plt
from calligraphy_transform import calligraphy_transform
from utils.tools import save_file

if __name__ == '__main__':
    path = '../../data/source/6/代.txt'
    output_path = '../../data/source/6/word.txt'

    calligraphy_tool = calligraphy_transform()
    z0_point = 0 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322]
    
    data_6d, data_cmd = calligraphy_tool.read_file(path, is_6dcmd=True)
    data_6d = calligraphy_tool.transform_6d(data_6d, z0_point, anchor=0, ratio=[1, 1, 0.6], translate=[0, 0, -2], angle=0)

    data_6d = calligraphy_tool.transform_to_rect_6d(data_6d, [-122, -65.5, 505, 543.5], z0_point, ratio_z=0, translate_z=0, center=True, deform=False)

    data_6d, data_cmd = calligraphy_tool.transform_6d_stroke(data_6d, data_cmd, 5, 6, z0_point, 0, ratio=[1, 1, 1], translate=[0, 6, 0], angle=0)
    
    calligraphy_tool.visualize_line_6d(data_6d, data_cmd, z0_point, with_thickness=True, plot=False)
    
    data_6dcmd = calligraphy_tool.six_to_cmd(data_6d, data_cmd)
    save_file(output_path, data_6dcmd)
    
    plt.gca().set_aspect("equal")
    plt.show()