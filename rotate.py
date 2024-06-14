import numpy as np
from numpy import cos, sin

class Rotation(object):
    def __init__(self, rotation_matrix=None):
        self.rotation_matrix = rotation_matrix
        self.T = np.transpose(self.rotation_matrix)

    def as_array(self):
        return self.rotation_matrix
    
    @classmethod
    def from_euler(cls, angles, seq:str='zyx', degrees:bool=False):
        if degrees:
            angles = np.asarray(angles) * (np.pi/180)

        mats = {'x':cls.__Rx, 'y':cls.__Ry, 'z':cls.__Rz}
        matrix = np.eye(3)
        for axis, angle in zip(seq, angles):
            matrix = np.dot(mats[axis](angle), matrix)
        R = cls(matrix)
        return R

    def __Rx(angle):
        Rx = np.array([[1, 0, 0],
                    [0, cos(angle), -sin(angle)],
                    [0, sin(angle), cos(angle)]
                    ])
        return Rx
    
    def __Ry(angle):
        Ry = np.array([[cos(angle), 0, sin(angle)],
                       [0, 1, 0],
                       [-sin(angle), 0, cos(angle)]])
        return Ry
    
    def __Rz(angle):
        Rz = np.array([[cos(angle), -sin(angle), 0],
                       [sin(angle), cos(angle), 0],
                       [0, 0, 1]])
        return Rz
    
if __name__ == "__main__":
    test = Rotation.from_euler([45, 0, 0], 'zyx', True)
    print(test.as_array())