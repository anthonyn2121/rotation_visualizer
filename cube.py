import argparse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from rotate import Rotation


def plot_cube(cube_vertices, ax=None, alpha=0.75, figsize=(5,5,5)):

    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
    if figsize:
        ax.set_xlim(-figsize[0]//2, figsize[0]//2+1)
        ax.set_ylim(-figsize[1]//2, figsize[1]//2+1)
        ax.set_zlim(-figsize[2]//2, figsize[2]//2+1)

    cube_faces = [
        [cube_vertices[j] for j in [0, 1, 5, 4]],
        [cube_vertices[j] for j in [7, 6, 2, 3]],
        [cube_vertices[j] for j in [0, 3, 7, 4]],
        [cube_vertices[j] for j in [1, 2, 6, 5]],
        [cube_vertices[j] for j in [0, 1, 2, 3]],
        [cube_vertices[j] for j in [4, 5, 6, 7]]
    ]

    face_colors = ['cyan', 'magenta', 'yellow', 'blue', 'green', 'red']
    for i, face in enumerate(cube_faces):
        face_vertices = np.array(face)
        ax.add_collection3d(Poly3DCollection([face_vertices], color=face_colors[i], alpha=alpha, edgecolor='k'))
    return ax


cube_vertices = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
])


if __name__ == "__main__":
    # Run this file to visualize rotation
    parser = argparse.ArgumentParser()
    parser.add_argument('--transforms', '-t', type=float, nargs='+', action='append', help="sequence of transformations. Must be ONLY euler angles or ONLY quaternions")
    parser.add_argument('--sequence', '-s', default='zyx', help="Order of axis to apply rotations")
    parser.add_argument('--degrees', '-d', type=bool, default=True, help="If using euler angles, are your angles expressed in degrees?")
    args = parser.parse_args()

    transformations = np.asarray(args.transforms)
    alpha = 0.5
    ax = plot_cube(cube_vertices, alpha=alpha)
    rotations = []
    if transformations.shape[1] == 3:
        rotations= [Rotation.from_euler(t, args.sequence, degrees=args.degrees) for t in transformations]
    elif transformations.shape[1] == 4:
        rotations= [Rotation.from_quat(t) for t in transformations]
    

    from matplotlib.animation import FuncAnimation
    def animate(frame):
        ax.clear()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        if len(rotations) > 0:
            rot = rotations[frame % len(rotations)]
            new_vertices = cube_vertices @ np.transpose(rot.as_array())
            plot_cube(new_vertices, ax=ax, alpha=alpha)
        else:
            plot_cube(cube_vertices, ax)

    anim = FuncAnimation(ax.get_figure(), animate, frames=len(rotations), interval=100)
    anim.save('cube_rotation.gif', fps=5)
    plt.show(block=True)