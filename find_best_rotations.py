import numpy as np
import itertools

N = 4

def get_pyramid():
    cubes = []
    for k in range(1, N + 1):
        for i in range(k):
            for j in range(k):
                cubes.append(np.array([j, -i, -k]))
    return cubes

A = get_pyramid()
A_set = set(tuple(c) for c in A)

# Generate all 24 3D rotations for integer coordinates
# A rotation matrix has one 1 or -1 in each row and column.
rotations = []
for p in itertools.permutations([0, 1, 2]):
    for signs in itertools.product([-1, 1], repeat=3):
        # check if determinant is 1
        mat = np.zeros((3, 3), dtype=int)
        for i in range(3):
            mat[i, p[i]] = signs[i]
        if np.linalg.det(mat) > 0:
            rotations.append(mat)

def apply_rot(cubes, rot_mat):
    return [np.dot(rot_mat, c) for c in cubes]

best_vol = float('inf')
best_combo = None

for rotB_idx, rotB in enumerate(rotations):
    B = apply_rot(get_pyramid(), rotB)
    # find valid offsets for B
    valid_B = []
    for dx in range(-N, N+2):
        for dy in range(-N, N+2):
            for dz in range(-N, N+2):
                offset_B = set(tuple(c + np.array([dx, dy, dz])) for c in B)
                if not A_set.intersection(offset_B):
                    valid_B.append((np.array([dx,dy,dz]), offset_B))
    
    for offset_B_vec, offset_B_set in valid_B:
        AB_set = A_set.union(offset_B_set)
        
        for rotC_idx, rotC in enumerate(rotations):
            C = apply_rot(get_pyramid(), rotC)
            # find valid offsets for C
            for dx in range(-N, N+2):
                for dy in range(-N, N+2):
                    for dz in range(-N, N+2):
                        offset_C = set(tuple(c + np.array([dx, dy, dz])) for c in C)
                        if not AB_set.intersection(offset_C):
                            union = AB_set.union(offset_C)
                            xs, ys, zs = zip(*union)
                            vol = (max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)*(max(zs)-min(zs)+1)
                            if vol < best_vol:
                                best_vol = vol
                                best_combo = {
                                    'rotB': rotB, 'offsetB': offset_B_vec,
                                    'rotC': rotC, 'offsetC': np.array([dx, dy, dz]),
                                    'shape': (max(xs)-min(xs)+1, max(ys)-min(ys)+1, max(zs)-min(zs)+1)
                                }

print("Best Volume:", best_vol)
print("Best Combo:", best_combo)
