import math
import numpy as np
import matplotlib.pyplot as plt

def save_file(data, out_path):

    output_data = list()

    for row in data:
        output_data.append(f"{str(row)[1:-1].replace(',', '')}\n")

    fp = open(out_path, "a")
    fp.writelines(output_data)
    fp.close()

def find_anchor(data):
    datax = [i[0] for i in data]
    datay = [i[1] for i in data]

    return [min(datax), max(datay), 10]

def angle2deg(angle):
    return angle * math.pi / 180 

def visualization_from_path(path):
    xyz = list()

    txtFile = open(path)
    for row in txtFile:
        xyz.append([float(i) for i in row.split()])
    
    plt.plot([i[0] for i in xyz], [i[1] for i in xyz], 'ro')
    plt.show()

def visualization_from_var(data):
    plt.plot([i[0] for i in data], [i[1] for i in data], 'ro')
    plt.show()

def six_to_three(sixd_path, out_path):
    data = []
    txtFile = open(sixd_path)
    for row in txtFile:

        row = row.split()
        x = float(row[2])
        y = float(row[3])
        z = float(row[4])
        a = angle2deg(float(row[5]))
        b = angle2deg(float(row[6]))
        c = angle2deg(float(row[7]))
        
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
        B = np.array([[0],[0],[185],[1]])

        T = np.dot(A, B)

        data.append([T[0][0], T[1][0], T[2][0]])

    return np.array(data)

def resize(data, anchor, ratio):
    out_data = list()
    
    affine1 = np.array([
        [1, 0, 0, -anchor[0]],
        [0, 1, 0, -anchor[1]],
        [0, 0, 1, -anchor[2]],
        [0, 0, 0, 1]
    ])

    affine2 = np.array([
        [ratio[0], 0, 0, anchor[0]],
        [0, ratio[1], 0, anchor[1]],
        [0, 0, ratio[2], anchor[2]],
        [0, 0, 0, 1]
    ])
    
    for row in data:
        row = np.append(row,1).reshape(4, 1)
        row = np.dot(affine1, row)
        row = np.dot(affine2, row)
        out_data.append([row[0][0], row[1][0], row[2][0]])

    return np.array(out_data)

if __name__ == '__main__':
    sixd_path = '../data/工.txt'
    out_path = '../output/test.txt'
    data = six_to_three(sixd_path, out_path)
    data = resize(data, find_anchor(data), [0.3, 0.3, 0.3])
    visualization_from_var(data)
    #data = resize(sixd_path)
    #save_file(data, out_path)
    #visualization(out_path)



    