import os, sys
sys.path.append('..')

import numpy as np
from calligraphy_transform import calligraphy_transform
from utils.tools import save_file

water_path = '../../data/source/water/water.txt'
startx = -250
starty = 400
total_width = 251
total_height = 92
end6dcmd = np.array([['cmd42', '0', '-105', '-22', '-70', '0', '-90', '0', '', '']])
axis = np.array([[startx, starty], [startx, starty+total_height], [startx+total_width, starty+total_height], [startx+total_width, starty]])

calligraphy_tool = calligraphy_transform()
water_6d, water_cmd = calligraphy_tool.read_file(water_path, is_6dcmd=True)
out_6dcmd = calligraphy_tool.six_to_cmd(water_6d, water_cmd)
sample_6d = np.array([[-169.6492231584243, 425.04838061558877, 166.73827137352038, -158.4866, -2.4102, 44.4074]])
sample_cmd = np.array([['movl', 0, 100.0000, 'stroke0']])
sample_3d, sample_angle = calligraphy_tool.six_to_three(sample_6d)

for i in range(len(axis)+1):
    for j in range(2):
        sample_3d[0][0] = axis[i%4][0]
        sample_3d[0][1] = axis[i%4][1]
        tmp_6d = calligraphy_tool.three_to_six(sample_3d, sample_angle)
        
        out_6dcmd = np.append(out_6dcmd, calligraphy_tool.six_to_cmd(tmp_6d, sample_cmd), 0)

sample_3d[0][2] += 50
tmp_6d = calligraphy_tool.three_to_six(sample_3d, sample_angle)
out_6dcmd = np.append(out_6dcmd, calligraphy_tool.six_to_cmd(tmp_6d, sample_cmd), 0)

out_6dcmd = np.append(out_6dcmd, end6dcmd, 0)

save_file(f'../../data/output/rect.txt', out_6dcmd)
