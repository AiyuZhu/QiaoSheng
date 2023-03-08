import math
import numpy as np

import materials
import pymeshlab


def calculate_mass(volume, material):
    if material == 'steel':
        den = materials.carbon_steel.density
        return volume * den


def calculate_volume(file_name, scale_factor=0.1):
    ms = pymeshlab.MeshSet()

    ms.load_new_mesh(file_name)

    # Scaling the mesh
    ms.compute_matrix_from_scaling_or_normalization(axisx=scale_factor, axisy=scale_factor, axisz=scale_factor)

    # Generating the convex hull of the mesh
    ms.generate_convex_hull()

    # Calculating intertia tensor
    geom = ms.get_geometric_measures()
    volume = geom['mesh_volume']

    return volume


def calculate_inertia(file_name, mass, scale_factor=100):
    ms = pymeshlab.MeshSet()

    ms.load_new_mesh(file_name)
    geom = ms.get_geometric_measures()
    co = geom['barycenter']

    # Scaling the mesh
    ms.compute_matrix_from_scaling_or_normalization(axisx=scale_factor, axisy=scale_factor, axisz=scale_factor)

    # Generating the convex hull of the mesh
    ms.generate_convex_hull()

    # Calculating intertia tensor
    geom = ms.get_geometric_measures()
    volume = geom['mesh_volume']
    tensor = geom['inertia_tensor'] / pow(scale_factor, 2) * mass / volume

    return \
        mass, tensor[0, 0], tensor[1, 0], tensor[2, 0], tensor[1, 1], tensor[1, 2], tensor[2, 2], co[0], co[1], co[2]


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


if __name__ == '__main__':
    print(calculate_inertia('C:\\Users\\Aiyu\\Desktop\\1v_ZCRjlL9pudQA7oZBgU5.dae', 0.01))
