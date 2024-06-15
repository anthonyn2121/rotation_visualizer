import numpy as np
from numpy import cos, sin

class Rotation(object):
    def __init__(self, rotation_matrix:np.array=None, quat:np.array=None):
        assert np.any(rotation_matrix) or np.any(quat), "RotationMatrix, Quaternion are both None"
        if np.any(rotation_matrix):
            assert rotation_matrix.shape == (3,3), "RotationMatrix is not a 3x3"
            self.rotation_matrix = rotation_matrix
            self.quat = self.__rotm2quat(self.rotation_matrix)
        elif np.any(quat):
            assert len(quat) == 4, "Quaternion does not have 4 elements"
            self.quat = quat
            self.rotation_matrix = self.__quat2rotm(self.quat)

    def as_array(self):
        return self.rotation_matrix
    
    def as_quat(self):
        return self.quat
    
    def inv(self):
        return Rotation(rotation_matrix=np.transpose(self.rotation_matrix))

    @classmethod
    def from_euler(cls, angles, seq:str='zyx', degrees:bool=False):
        if degrees:
            angles = np.asarray(angles) * (np.pi/180)

        mats = {'x':cls.__Rx, 'y':cls.__Ry, 'z':cls.__Rz}
        matrix = np.eye(3)
        for axis, angle in zip(seq, angles):
            matrix = mats[axis](angle) @ matrix
        R = cls(rotation_matrix=matrix)
        return R

    @classmethod
    def from_quat(cls, quat):
        R = cls(quat=quat)
        return R

    def __rotm2quat(self, matrix):
        R = matrix
        trace = np.trace(R)
        if (trace > 0):
            s = 0.5 / np.sqrt(trace + 1.0)
            w = 0.25 / s
            x = (R[2, 1] - R[1, 2]) * s
            y = (R[0, 2] - R[2, 0]) * s
            z = (R[1, 0] - R[0, 1]) * s
        else:
            if (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):
                s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
                w = (R[2, 1] - R[1, 2]) / s
                x = 0.25 * s
                y = (R[0, 1] + R[1, 0]) / s
                z = (R[0, 2] + R[2, 0]) / s
            elif R[1, 1] > R[2, 2]:
                s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
                w = (R[0, 2] - R[2, 0]) / s
                x = (R[0, 1] + R[1, 0]) / s
                y = 0.25 * s
                z = (R[1, 2] + R[2, 1]) / s
            else:
                s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
                w = (R[1, 0] - R[0, 1]) / s
                x = (R[0, 2] + R[2, 0]) / s
                y = (R[1, 2] + R[2, 1]) / s
                z = 0.25 * s
        return np.array([x, y, z, w])

    def __quat2rotm(self, quat):
        x, y, z, w = quat
        m = np.array([[1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
                      [2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
                      [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2]])
        return m

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
    ## Run this file just to test
    test = Rotation.from_euler([45, 0, 0], 'zyx', True)
    print(test.as_array())