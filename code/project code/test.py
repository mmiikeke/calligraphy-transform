import matplotlib.pyplot as plt
import numpy as np
from calligraphy_transform import calligraphy_transform
from utils.tools import save_file

if __name__ == '__main__':
    index = [4,5,6,7,0,1,2,3]
    paths = ['../data/0/tt.txt', '../data/1/tt.txt', '../data/2/tt.txt', '../data/3/tt.txt', '../data/4/tt.txt', '../data/5/tt.txt', '../data/6/tt.txt', '../data/7/tt.txt']
    words = ['韌','性','城','鄉','工','業','代','謝']
    water_path = '../data/water/water.txt'
    #end6dcmd = np.array([['movl', 0, -111.143, 315.508, 333.159, 176.705, 0.0, -178.533, 100.0, 'strokeEnd']])
    end6dcmd = np.array([['cmd42', '0', '-105', '-22', '-70', '0', '-90', '0', '', '']])
    calligraphy_tool = calligraphy_transform()
    water_6d, water_cmd = calligraphy_tool.read_file(water_path, is_6dcmd=True)
    rects = list()
    
    startx = -250
    starty = 400
    total_width = 251
    total_height = 92
    padx = 5
    pady = 5

    width = (total_width - padx*5)/4
    height = (total_height - pady*3)/2

    for i in range(2):
        flagx = startx
        flagy = starty + i * (pady + height)
        for j in range(4):
            xs = flagx + padx
            xl = xs + width
            flagx = xl
            ys = flagy + pady
            yl = ys + height
            rects.append([xs, xl, ys, yl])
    
    plt.figure(figsize=(10,3.66))
    
    for rect in rects:
        x = [rect[0], rect[1], rect[1], rect[0], rect[0]]
        y = [rect[2], rect[2], rect[3], rect[3], rect[2]]
        plt.plot(x, y, c='k')
    
    rects[7][0] += 1
    rects[7][1] -= 1
    rects[7][2] += 1
    rects[7][3] -= 1

    rects[4][0] += 5
    rects[4][1] -= 5
    rects[4][2] += 5
    rects[4][3] -= 5

    rects[3][0] += 1
    rects[3][1] -= 1
    rects[3][2] += 1
    rects[3][3] -= 1

    rects[0][0] += 1
    rects[0][1] -= 1
    rects[0][2] += 1
    rects[0][3] -= 1

    z0_point = 0 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322]

    for i in index:
        data_6d, data_cmd = calligraphy_tool.read_file(paths[i], is_6dcmd=True)
        data_3d, data_angle = calligraphy_tool.six_to_three(data_6d)
        data_3d_transformed = calligraphy_tool.transform_to_rect_3d(data_3d, rects[i], z0_point, ratio_z=0, translate_z=-1, center=True, deform=False)

        tmpz = 0

        if i == 0: #韌
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[-2, 0, 0] ,thresholdZ=tmpz)
        if i == 1: #性
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, -2, -0.7] ,thresholdZ=tmpz)
        if i == 2: #城
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, 0, -1.2] ,thresholdZ=tmpz)
        if i == 3: #鄉
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, 0, -1.5] ,thresholdZ=tmpz)
        if i == 4: #工
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, -2, -0.6] ,thresholdZ=tmpz)
        if i == 5: #業
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, -2, -2.8] ,thresholdZ=tmpz)
        if i == 6: #代
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, 0, -2] ,thresholdZ=tmpz)
        if i == 7: #謝
            data_3d_transformed = calligraphy_tool.transform_3d(data_3d_transformed, translate=[0, 0, -2.5] ,thresholdZ=tmpz)

        data_6d = calligraphy_tool.three_to_six(data_3d_transformed, data_angle)
        output_6d, output_cmd = calligraphy_tool.data_6d_cmd_concate(data_6d, water_6d, data_cmd, water_cmd)
        output_6dcmd = calligraphy_tool.six_to_cmd(output_6d, output_cmd)
        for j in range(len(output_6dcmd)):
            output_6dcmd[j][-2] = 350.0
        output_6dcmd = np.append(output_6dcmd, end6dcmd, 0)
        save_file(f'../data/output2/{words[i]}.txt', output_6dcmd)

        calligraphy_tool.visualize_line_3d(data_3d_transformed, data_cmd, z0_point, with_thickness=True, plot=False)
        print(i)

        if i == 4:
            final_output = output_6dcmd
        else:
            final_output = np.append(final_output, output_6dcmd, 0)
    
    save_file(f'../data/output2/final.txt', final_output)
    
    plt.xlim(startx, startx + total_width)
    plt.ylim(starty, starty + total_height)
    plt.gca().set_aspect("equal")
    plt.show()
