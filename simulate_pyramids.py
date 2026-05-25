import numpy as np

N = 4

def get_pyramid():
    cubes = []
    for k in range(1, N + 1):
        for i in range(k):
            for j in range(k):
                cubes.append(np.array([j, -i, -k]))
    return cubes

# A is unchanged
A = get_pyramid()

# B: Rotate 180X, 90Z
def rot_x_180(v): return np.array([v[0], -v[1], -v[2]])
def rot_z_90(v): return np.array([-v[1], v[0], v[2]])
B = [rot_z_90(rot_x_180(v)) for v in get_pyramid()]

# C: Rotate 90Y, 180Z
def rot_y_90(v): return np.array([v[2], v[1], -v[0]])
def rot_z_180(v): return np.array([-v[0], -v[1], v[2]])
C = [rot_z_180(rot_y_90(v)) for v in get_pyramid()]

# Let's find exactly the offsets so they interlock perfectly
# A is at origin
valid_B = []
A_set = set(tuple(c) for c in A)
for dx in range(-10, 10):
    for dy in range(-10, 10):
        for dz in range(-10, 10):
            offset_B = set(tuple(c + np.array([dx,dy,dz])) for c in B)
            if not A_set.intersection(offset_B):
                valid_B.append((dx,dy,dz))

min_vol_B = float('inf')
best_B = None
for offset in valid_B:
    offset_B = set(tuple(c + np.array(offset)) for c in B)
    union = A_set.union(offset_B)
    xs, ys, zs = zip(*union)
    vol = (max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)*(max(zs)-min(zs)+1)
    if vol < min_vol_B:
        min_vol_B = vol
        best_B = offset

print("Best B offset:", best_B)

offset_B = set(tuple(c + np.array(best_B)) for c in B)
AB_set = A_set.union(offset_B)

valid_C = []
for dx in range(-10, 10):
    for dy in range(-10, 10):
        for dz in range(-10, 10):
            offset_C = set(tuple(c + np.array([dx,dy,dz])) for c in C)
            if not AB_set.intersection(offset_C):
                valid_C.append((dx,dy,dz))

min_vol_C = float('inf')
best_C = None
for offset in valid_C:
    offset_C = set(tuple(c + np.array(offset)) for c in C)
    union = AB_set.union(offset_C)
    xs, ys, zs = zip(*union)
    vol = (max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)*(max(zs)-min(zs)+1)
    if vol < min_vol_C:
        min_vol_C = vol
        best_C = offset

print("Best C offset:", best_C)
offset_C = set(tuple(c + np.array(best_C)) for c in C)
ABC_set = AB_set.union(offset_C)

xs, ys, zs = zip(*ABC_set)
print(f"Final shape: X:[{min(xs)}, {max(xs)}] Y:[{min(ys)}, {max(ys)}] Z:[{min(zs)}, {max(zs)}]")
