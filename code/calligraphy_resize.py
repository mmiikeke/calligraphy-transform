import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.tools import save_file

def read_file(path, is_6dcmd = True):
    data = list()
    txtFile = open(path)

    if is_6dcmd:
        cmd = list()
        for row in txtFile:
            row = row.split()
            data.append([float(row[2]), float(row[3]), float(row[4]), 
                        float(row[5]), float(row[6]), float(row[7])])
            cmd.append([row[0], row[1], row[8], row[9]])
        
        return np.array(data), np.array(cmd)
    
    else:
        for row in txtFile:
            data.append([float(i) for i in row.split()])
        return np.array(data)
        
def find_anchor(data_3d, z):
    datax = [i[0] for i in data_3d]
    datay = [i[1] for i in data_3d]

    return [min(datax), max(datay), z]

def angle2deg(angle):
    return angle * math.pi / 180 

def find_draw_points(data_3d, data_cmd, thresholdZ):
    output_data_3d = list()
    output_data_cmd = list()

    for i, _ in enumerate(data_3d):
        if data_3d[i][-1] < thresholdZ:
            output_data_3d.append(data_3d[i])
            output_data_cmd.append(data_cmd[i])

    return np.array(output_data_3d), np.array(output_data_cmd)

def find_stroke(data_cmd):
    stroke = [0]
    flag = data_cmd[0][-1]

    for i, data in enumerate(data_cmd):
        if flag != data[-1]:
            stroke.append(i)
            flag = data[-1]

    return stroke

def visualize(data_3d):
    plt.plot([i[0] for i in data_3d], [i[1] for i in data_3d], 'ro')
    plt.show()

def visualize_line(data_3d, data_cmd, thresholdZ, with_thickness = False):
    data_3d, data_cmd = find_draw_points(data_3d, data_cmd, thresholdZ)
    
    stroke = find_stroke(data_cmd)
    
    if not with_thickness: 
        for i in range(len(stroke)-1):
            line = data_3d[stroke[i]:stroke[i+1]]
            plt.plot([i[0] for i in line], [i[1] for i in line], c='darkslategray')
    else:
        for i in range(len(data_3d)-1):
            if not (i+1 in stroke):
                x = [data_3d[i][0], data_3d[i+1][0]]
                y = [data_3d[i][1], data_3d[i+1][1]]
                width = (thresholdZ - ((data_3d[i][2] + data_3d[i+1][2])*0.5))*2
                plt.plot(x, y, linewidth=width, c='darkslategray')
    plt.show()

def six_to_cmd(data_6d, data_cmd):
    data_6dcmd = list()
    len_data = len(data_6d)

    for i in range(len_data):
        data_6dcmd.append([
            data_cmd[i][0],
            data_cmd[i][1],
            data_6d[i][0],
            data_6d[i][1],
            data_6d[i][2],
            data_6d[i][3],
            data_6d[i][4],
            data_6d[i][5],
            data_cmd[i][2],
            data_cmd[i][3]
            ])
    
    return data_6dcmd

def three_to_six(data_3d, data_angle, length = [0,0,-185]):
    data_concate = np.append(data_3d, data_angle, 1)
    out_data_3d, _ = six_to_three(data_concate, length)
    out_data_6d = np.append(out_data_3d, data_angle, 1)

    return out_data_6d

def six_to_three(data_6d, length = [0,0,185]):
    data_3d = list()
    data_angle = list()

    for row in data_6d:

        x = row[0]
        y = row[1]
        z = row[2]
        a = angle2deg(row[3])
        b = angle2deg(row[4])
        c = angle2deg(row[5])
        
        Ra = np.array([
            [1, 0, 0],
            [0, math.cos(a), -math.sin(a)],
            [0, math.sin(a), math.cos(a)]
        ])

        Rb = np.array([
            [math.cos(b), 0, math.sin(b)],
            [0, 1, 0],
            [-math.sin(b), 0, math.cos(b)]
        ])

        Rc = np.array([
            [math.cos(c), -math.sin(c), 0],
            [math.sin(c), math.cos(c), 0],
            [0, 0, 1]
        ])
        
        R = np.dot(np.dot(Rc, Rb), Ra)
        
        A = np.array([
            [R[0, 0], R[0, 1], R[0, 2], x],
            [R[1, 0], R[1, 1], R[1, 2], y],
            [R[2, 0], R[2, 1], R[2, 2], z],
        ])

        # 毛筆為 x軸 0mm, y軸 0mm, z軸 185 mm
        B = np.array([[length[0]],[length[1]],[length[2]],[1]])

        T = np.dot(A, B)

        data_3d.append([T[0][0], T[1][0], T[2][0]])
        data_angle.append([row[3], row[4], row[5]])

    return np.array(data_3d), np.array(data_angle)

def resize(data, anchor, ratio, translate):
    out_data = list()
    
    affine1 = np.array([
        [1, 0, 0, -anchor[0]],
        [0, 1, 0, -anchor[1]],
        [0, 0, 1, -anchor[2]],
        [0, 0, 0, 1]
    ])

    affine2 = np.array([
        [ratio[0], 0, 0, anchor[0]+translate[0]],
        [0, ratio[1], 0, anchor[1]+translate[1]],
        [0, 0, ratio[2], anchor[2]+translate[2]],
        [0, 0, 0, 1]
    ])
    
    for row in data:
        row = np.append(row,1).reshape(4, 1)
        row = np.dot(affine1, row)
        row = np.dot(affine2, row)
        out_data.append([row[0][0], row[1][0], row[2][0]])

    return np.array(out_data)

if __name__ == '__main__':
    in_6dcmd_path = '../data/代.txt'
    out_3d_path = '../output/代3d.txt'
    out_3dresized_path = '../output/代3dresized.txt'
    out_6dcmd_path = '../output/代6dcmd.txt'

    z0_point = 5.5 #3.21083745
    """
    data = np.array([[-66.7041, 438.85, 187.479, -177.603, 4.50068, -9.48322]])
    data = six_to_three(data)
    for i in data:
        print(i)
    """
    data_6d, data_cmd = read_file(in_6dcmd_path, is_6dcmd=True)

    data_3d, data_angle = six_to_three(data_6d)

    visualize_line(data_3d, data_cmd, z0_point, with_thickness=True)

    """
    data_6d, data_cmd = read_file(in_6dcmd_path, is_6dcmd=True)

    data_3d, data_angle = six_to_three(data_6d)
    save_file(out_3d_path, data_3d)
    #visualize(data_3d)

    data_3d = resize(data_3d, find_anchor(data_3d, z0_point), [0.5, 0.5, 0.35], [0, 100, -4])
    save_file(out_3dresized_path, data_3d)
    #visualize(data_3d)
    
    data_6d = three_to_six(data_3d, data_angle)
    data_6dcmd = six_to_cmd(data_6d, data_cmd)
    save_file(out_6dcmd_path, data_6dcmd)
    """


    