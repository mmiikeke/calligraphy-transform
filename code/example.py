import matplotlib.pyplot as plt
from calligraphy_transform import callifraphy_transform
from utils.tools import save_file

if __name__ == '__main__':
    path = '../data/代.txt'
    output_path1 = '../o/3d.txt'
    output_path2 = '../o/3d_1.txt'
    output_path3 = '../o/3d_2.txt'
    output_path4 = '../o/6dcmd.txt'

    calligraphy_tool = callifraphy_transform()
    z0_point = 5.5 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322]
    data_6d, data_cmd = calligraphy_tool.read_file(path, is_6dcmd=True)
    data_3d, data_angle = calligraphy_tool.six_to_three(data_6d)
    calligraphy_tool.visualize_line(data_3d, data_cmd, z0_point, with_thickness=True)
    save_file(output_path1, data_3d)

    data_3d_transformed = calligraphy_tool.transform(data_3d, anchor=calligraphy_tool.find_anchor(data_3d, z0_point), ratio=[0.5, 0.5, 0.35], translate=[0, 0, 0])
    calligraphy_tool.visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True)
    save_file(output_path2, data_3d_transformed)


    data_3d_transformed = calligraphy_tool.transform_to_rect(data_3d, [-40,40,-40,40], z0_point, ratio_z=0, translate_z=0, center=True, deform=False)
    calligraphy_tool.visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True)
    save_file(output_path3, data_3d_transformed)
    
    data_6d = calligraphy_tool.three_to_six(data_3d_transformed, data_angle)
    data_6dcmd = calligraphy_tool.six_to_cmd(data_6d, data_cmd)
    save_file(output_path4, data_6dcmd)