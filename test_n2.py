import numpy as np
import itertools

N = 2

def get_pyramid():
    cubes = []
    for k in range(1, N + 1):
        for i in range(k):
            for j in range(k):
                cubes.append((j, i, k-1))
    return cubes

base_pyr = get_pyramid()

rotations = []
for p in itertools.permutations([0, 1, 2]):
    for signs in itertools.product([-1, 1], repeat=3):
        mat = np.zeros((3, 3), dtype=int)
        for i in range(3): mat[i, p[i]] = signs[i]
        if np.linalg.det(mat) > 0: rotations.append(mat)

grid_shape = (N, N+1, 2*N+1)
grid_vol = grid_shape[0]*grid_shape[1]*grid_shape[2]

placements = []
for rot in rotations:
    rot_pyr = [np.dot(rot, c) for c in base_pyr]
    xs, ys, zs = zip(*rot_pyr)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    
    shifted = [(x - min_x, y - min_y, z - min_z) for x, y, z in rot_pyr]
    width = max_x - min_x + 1
    depth = max_y - min_y + 1
    height = max_z - min_z + 1
    
    for dx in range(grid_shape[0] - width + 1):
        for dy in range(grid_shape[1] - depth + 1):
            for dz in range(grid_shape[2] - height + 1):
                placement = [(x+dx, y+dy, z+dz) for x, y, z in shifted]
                indices = tuple(sorted(x + y*grid_shape[0] + z*grid_shape[0]*grid_shape[1] for x,y,z in placement))
                placements.append((rot, dx, dy, dz, indices))

unique_placements = []
seen = set()
for p in placements:
    if p[4] not in seen:
        seen.add(p[4])
        unique_placements.append(p)

solution = []
def solve(idx, current_mask):
    if len(solution) == 6:
        return True
    
    for i in range(idx, len(unique_placements)):
        p = unique_placements[i]
        indices = p[4]
        overlap = False
        for pos in indices:
            if current_mask[pos]:
                overlap = True
                break
        
        if not overlap:
            for pos in indices: current_mask[pos] = True
            solution.append(p)
            if solve(i + 1, current_mask): return True
            solution.pop()
            for pos in indices: current_mask[pos] = False
    return False

mask = [False] * grid_vol
if solve(0, mask):
    print("Found solution for N=2!")
    for s in solution:
        print("Rot:", s[0].tolist(), "Offset:", s[1:4])
else:
    print("No solution found for N=2!")
