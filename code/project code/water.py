import matplotlib.pyplot as plt
from calligraphy_transform import calligraphy_transform
from utils.tools import save_file

def stroke_transformation(data_6d, data_cmd, stroke_start, stroke_end, ratio=[1, 1, 1], translate=[0, 0, 0], angle=0):
    data_6d_1, data_6d_2, data_cmd_1, data_cmd_2 = calligraphy_tool.data_6d_cmd_split(data_6d, data_cmd, stroke_start, stroke_end)
    
    data_3d_2, data_angle_2 = calligraphy_tool.six_to_three(data_6d_2)
    data_3d_2 = calligraphy_tool.transform_3d(data_3d_2, calligraphy_tool.find_anchor(data_3d_2, z0_point), ratio, translate, angle)
    data_6d_2 = calligraphy_tool.three_to_six(data_3d_2, data_angle_2)

    data_6d, data_cmd = calligraphy_tool.data_6d_cmd_concate(data_6d_1, data_6d_2, data_cmd_1, data_cmd_2, stroke_start-1)

    return data_6d, data_cmd


if __name__ == '__main__':
    path = '../data/water/Big_water2_重新排列.txt'
    output_path1 = '../data/water/01_3d.txt'
    output_path2 = '../data/water/01_3d_2.txt'
    output_path3 = '../data/water/01_6d.txt' #=water.txt
    output_path4 = '../o/6dcmd.txt' 

    calligraphy_tool = calligraphy_transform()
    z0_point = 40 #3.21083745 [-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322] -2.85887236e-03 [-130.099, 459.278,182.715,175.55,-7.84099,70.2961]
    data_6d, data_cmd = calligraphy_tool.read_file(path, is_6dcmd=True)
    data_3d, data_angle = calligraphy_tool.six_to_three(data_6d)
    calligraphy_tool.visualize_line_3d(data_3d, data_cmd, z0_point, with_thickness=False)
    #save_file(output_path1, data_3d)
    
    data_3d_transformed = calligraphy_tool.transform_3d(data_3d, anchor=calligraphy_tool.find_anchor(data_3d, z0_point), ratio=[1, 1, 1], translate=[0, 0, 10])
    data_6d = calligraphy_tool.three_to_six(data_3d_transformed, data_angle)

    data_6d, data_cmd = stroke_transformation(data_6d, data_cmd, 1, 2, ratio=[1, 1, 1], translate=[0, 0, -5], angle=0)
    data_6d, data_cmd = stroke_transformation(data_6d, data_cmd, 4, 8, ratio=[1, 1, 1], translate=[0, 0, -15], angle=0)

    data_6dcmd = calligraphy_tool.six_to_cmd(data_6d, data_cmd)
    #calligraphy_tool.visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True)
    #save_file(output_path2, data_3d_transformed)


    #data_3d_transformed = calligraphy_tool.transform_to_rect(data_3d, [-40,40,-40,40], z0_point, ratio_z=0, translate_z=0, center=True, deform=False)
    #calligraphy_tool.visualize_line(data_3d_transformed, data_cmd, z0_point, with_thickness=True)
    #save_file(output_path3, data_3d_transformed)
    
    #data_6d = calligraphy_tool.three_to_six(data_3d_transformed, data_angle)
    #data_6dcmd = calligraphy_tool.six_to_cmd(data_6d, data_cmd)
    save_file(output_path3, data_6dcmd)
    