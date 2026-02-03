import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Create a figure and a 3D Axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the vertices of a cube
r = [-1, 1]
vertices = np.array([[x, y, z] for x in r for y in r for z in r])

# Define the edges of the cube
edges = [
    [vertices[j] for j in [0, 1, 3, 2, 0]],
    [vertices[j] for j in [4, 5, 7, 6, 4]],
    [vertices[j] for j in [0, 1, 5, 4, 0]],
    [vertices[j] for j in [2, 3, 7, 6, 2]],
    [vertices[j] for j in [1, 3, 7, 5, 1]],
    [vertices[j] for j in [0, 2, 6, 4, 0]]
]

# Initialize the plot
lines = []
for edge in edges:
    line, = ax.plot3D(*zip(*edge), color="b")
    lines.append(line)

# Animation function: called sequentially
def update(num, lines, vertices):
    angle = np.radians(num)
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    
    rotated_vertices = vertices @ rotation_matrix.T
    for line, edge in zip(lines, edges):
        line.set_data(rotated_vertices[edge][:, :2].T)
        line.set_3d_properties(rotated_vertices[edge][:, 2])
    return lines

# Create an animation
ani = animation.FuncAnimation(fig, update, frames=180, fargs=(lines, vertices), interval=50)

# Set the plot limits and labels
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the animation
plt.show()
