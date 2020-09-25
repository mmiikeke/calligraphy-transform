import math
import numpy as np
import matplotlib.pyplot as plt

def visualization(path):
    xy = list()

    txtFile = open(path)
    for row in txtFile:
        xy.append([float(i) for i in row.split()])
    
    plt.plot([i[0] for i in xy], [i[1] for i in xy], 'ro')
    plt.show()

def angle2deg(angle):
    return angle * math.pi / 180 

def six_to_three(sixd_path, out_path):
    data = []
    with open(sixd_path) as txtFile:
        for row in txtFile:

            row = row.lstrip().split(' ')
            x = float(row[2])
            y = float(row[3])
            z = float(row[4])
            a = angle2deg(float(row[5]))
            b = angle2deg(float(row[6]))
            c = angle2deg(float(row[7]))
            
            Ra = [1, 0, 0,
                0, math.cos(a), -1 * math.sin(a),  
                0, math.sin(a), math.cos(a)      ]

            Rb = [math.cos(b), 0, math.sin(b),
                0, 1, 0,  
                -1 * math.sin(b), 0, math.cos(b)      ]

            Rc = [math.cos(c), -1 * math.sin(c), 0,
                math.sin(c), math.cos(c), 0,  
                0, 0, 1      ]

            Ra = np.array(Ra).reshape(3, 3)
            Rb = np.array(Rb).reshape(3, 3)
            Rc = np.array(Rc).reshape(3, 3)
            
            R = np.dot(np.dot(Rc, Rb), Ra)
            
            A = [R[0, 0], R[0, 1], R[0, 2], x,
                R[1, 0], R[1, 1], R[1, 2], y,
                R[2, 0], R[2, 1], R[2, 2], z,
                0, 0, 0, 1]
            A = np.array(A).reshape((4, 4))

            B = np.identity(4)
            B[2, 3] = 185 # 毛筆長度 185 mm

            T = np.dot(A, B)

            data.append(f'{T[0, 3]} {T[1, 3]} {T[2, 3]}\n')

    fp = open(out_path, "a")
 
    fp.writelines(data)

    fp.close()
    


if __name__ == '__main__':
    sixd_path = '../data/工.txt'
    out_path = '../output/test.txt'
    #six_to_three(sixd_path, out_path)
    #visualization(out_path)



    