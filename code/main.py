import matplotlib.pyplot as plt
from calligraphy_transform import callifraphy_transform

if __name__ == '__main__':
    index = [1,2,4,6,7]
    paths = ['', '../data/性.txt', '../data/城.txt', '', '../data/工.txt', '', '../data/代.txt', '../data/謝.txt']
    rects = list()
    
    startx = 0
    starty = 0
    total_width = 251
    total_height = 92
    padx = 10
    pady = 10

    width = (total_width - padx*5)/4
    height = (total_height - pady*3)/2

    for i in range(2):
        flagx = 0
        flagy = i * (pady + height)
        for j in range(4):
            xs = flagx + padx
            xl = xs + width
            flagx = xl
            ys = flagy + pady
            yl = ys + height
            rects.append([xs, xl, ys, yl])
    
    rects[4][0] += 5
    rects[4][1] -= 5
    rects[4][2] += 5
    rects[4][3] -= 5


    calligraphy_tool = callifraphy_transform()

    z0_point = 5.5 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322]

    plt.figure(figsize=(10,3.66))

    for i in index:
        data_6d, data_cmd = calligraphy_tool.read_file(paths[i], is_6dcmd=True)
        data_3d, data_angle = calligraphy_tool.six_to_three(data_6d)
        data_3d_transformed = calligraphy_tool.transform_to_rect(data_3d, rects[i], z0_point, ratio_z=0.3, translate_z=0, center=False, deform=False)

        if i == 1: #性
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, -2, 0])

        if i == 4: #工
            data_3d_transformed = calligraphy_tool.transform(data_3d_transformed, translate=[0, -2, 0])

        calligraphy_tool.visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True, plot=False)
        print(i)
    
    plt.xlim(startx, total_width)
    plt.ylim(starty, total_height)
    plt.show()
    #data_6d, data_cmd = calligraphy_tool.read_file(path, is_6dcmd=True)
    #data_3d, data_angle = calligraphy_tool.six_to_three(data_6d)
    #visualize_line(data_3d, data_cmd, z0_point, with_thickness=True)
    #save_file(out_3d_path, data_3d)

    #data_3d_transformed = transform(data_3d, anchor=find_anchor(data_3d, z0_point), ratio=[0.5, 0.5, 0.35], translate=[0, 0, 0])
    #data_3d_transformed = transform_to_rect(data_3d, [-40,40,-40,40], z0_point, ratio_z=0, translate_z=0, center=False, deform=False)
    #visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True)
    #save_file(out_3dtransformed_path, data_3d_transformed)
    
    #data_6d = three_to_six(data_3d_transformed, data_angle)
    #data_6dcmd = six_to_cmd(data_6d, data_cmd)
    #save_file(out_6dcmd_path, data_6dcmd)
