import matplotlib.pyplot as plt
from calligraphy_transform import callifraphy_transform
from utils.tools import save_file

if __name__ == '__main__':
    index = [0,1,2,3,4,5,6,7]
    paths = ['../data/0/char00649_stroke_5_18.txt', '../data/性.txt', '../data/城.txt', '../data/3/char00423_stroke_1_15.txt', '../data/工.txt', '../data/5/char00537_stroke_3_15.txt', '../data/代.txt', '../data/謝.txt']
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

    calligraphy_tool = callifraphy_transform()

    z0_point = 3.5 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322]

    for i in index:
        data_6d, data_cmd = calligraphy_tool.read_file(paths[i], is_6dcmd=True)
        data_3d, data_angle = calligraphy_tool.six_to_three(data_6d)

        if i == 3: #鄉
            data_3d = calligraphy_tool.transform(data_3d, anchor=calligraphy_tool.find_anchor(data_3d, z0_point), ratio=[0.75, 1, 1], translate=[0, 0, -2.5])
        if i == 7: #謝
            data_3d = calligraphy_tool.transform(data_3d, anchor=calligraphy_tool.find_anchor(data_3d, z0_point), ratio=[1.1, 1, 1], translate=[0, 0, 0])

        data_3d_transformed = calligraphy_tool.transform_to_rect(data_3d, rects[i], z0_point, ratio_z=0.3, translate_z=0, center=True, deform=False)

        if i == 0: #韌
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, 0, 0])
        if i == 1: #性
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, -2, 0])
        if i == 2: #城
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, 0, 0.5])
        if i == 3: #鄉
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, 0, 0])
        if i == 4: #工
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, -2, 0])
        if i == 5: #業
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, 0, 0])
        if i == 6: #代
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, 0, 0])
        if i == 7: #謝
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, 0, 0])

        data_6d = calligraphy_tool.three_to_six(data_3d_transformed, data_angle)
        data_6dcmd = calligraphy_tool.six_to_cmd(data_6d, data_cmd)
        save_file(f'../data/output/{i}.txt', data_6dcmd)

        calligraphy_tool.visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True, plot=False)
        print(i)
    
    plt.xlim(startx, startx + total_width)
    plt.ylim(starty, starty + total_height)
    plt.gca().set_aspect("equal")
    plt.show()
