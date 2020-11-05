import os, sys
sys.path.append('..')

import matplotlib.pyplot as plt
from calligraphy_transform import calligraphy_transform
from utils.tools import save_file

if __name__ == '__main__':
    path = '../../data/source/0/char00649_stroke_5_14.txt'
    path2 = '../../data/source/0/char00496_stroke_3_6_.txt'
    output_path = '../../data/source/0/word.txt'

    calligraphy_tool = calligraphy_transform()
    z0_point = 0
    
    data_6d_1, data_cmd_1 = calligraphy_tool.read_file(path, is_6dcmd=True)
    data_6d_1 = calligraphy_tool.transform_6d(data_6d_1, z0_point, anchor=0, ratio=[1, 1, 0.6], translate=[0, 0, -3], angle=0)
    
    data_6d_2, data_cmd_2 = calligraphy_tool.read_file(path2, is_6dcmd=True)
    data_6d_2 = calligraphy_tool.transform_6d(data_6d_2, z0_point, anchor=0, ratio=[0.7, 0.85, 0.6], translate=[6, 4, -3], angle=2)

    data_6d_3, data_cmd_3 = calligraphy_tool.data_6d_cmd_concate(data_6d_2, data_6d_1, data_cmd_2, data_cmd_1)
    data_6d_3 = calligraphy_tool.transform_to_rect_6d(data_6d_3, [-244, -189.5, 406, 442.5], z0_point, ratio_z=0, translate_z=0, center=True, deform=False)

    calligraphy_tool.visualize_line_6d(data_6d_3, data_cmd_3, z0_point, with_thickness=True, plot=False)

    data_6dcmd = calligraphy_tool.six_to_cmd(data_6d_3, data_cmd_3)
    save_file(output_path, data_6dcmd)

    plt.gca().set_aspect("equal")
    plt.show()