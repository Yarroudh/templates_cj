import numpy as np

# Define function to convert Euler angles to rotation matrix
def euler_to_rotation_matrix(gamma, beta, alpha):
    # Convert angles to radians
    gamma = np.radians(gamma)
    beta = np.radians(beta)
    alpha = np.radians(alpha)
    
    # Rotation about Z-axis
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                   [np.sin(gamma), np.cos(gamma), 0],
                   [0, 0, 1]])
    
    # Rotation about Y-axis
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)],
                   [0, 1, 0],
                   [-np.sin(beta), 0, np.cos(beta)]])
    
    # Rotation about X-axis
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(alpha), -np.sin(alpha)],
                   [0, np.sin(alpha), np.cos(alpha)]])
    
    # Combined rotation matrix
    R = np.dot(Rz, np.dot(Ry, Rx))
    
    return R


# Define function to read ASCII OBJ file
def read_obj(file):
    vertices = []
    faces = []

    with open(file, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(i) for i in line.strip().split()[1:]]
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]
                faces.append(face)

    return vertices, faces
