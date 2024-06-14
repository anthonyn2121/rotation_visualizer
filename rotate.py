import numpy as np
from numpy import cos, sin

class Rotation(object):
    def __init__(self):
        pass

    @staticmethod
    def from_euler(angles, seq:str='zyx', degrees:bool=False):
        if degrees:
            angles = np.asarray(angles) * (np.pi/180)

        mats = {'x':Rotation._Rx, 'y':Rotation._Ry, 'z':Rotation._Rz}
        matrix = np.eye(3)
        for axis, angle in zip(seq, angles):
            matrix = np.dot(mats[axis](angle), matrix)
        return matrix

    @staticmethod
    def __Rx(angle):
        Rx = np.array([[1, 0, 0],
                    [0, cos(angle), -sin(angle)],
                    [0, sin(angle), cos(angle)]
                    ])
        return Rx
    
    @staticmethod
    def __Ry(angle):
        Ry = np.array([[cos(angle), 0, sin(angle)],
                       [0, 1, 0],
                       [-sin(angle), 0, cos(angle)]])
        return Ry
    
    @staticmethod
    def __Rz(angle):
        Rz = np.array([[cos(angle), -sin(angle), 0],
                       [sin(angle), cos(angle), 0],
                       [0, 0, 1]])
        return Rz
    
if __name__ == "__main__":
    print(Rotation._Rx(np.pi))