import numpy as np

N = 4

def get_pyramid():
    cubes = []
    for k in range(1, N + 1):
        for i in range(k):
            for j in range(k):
                cubes.append((j, -i, -k))
    return cubes

def rotate_x_180(cubes):
    return [(x, -y, -z) for x, y, z in cubes]

def rotate_z_90(cubes):
    return [(-y, x, z) for x, y, z in cubes]

def rotate_y_90(cubes):
    return [(z, y, -x) for x, y, z in cubes]

def rotate_z_180(cubes):
    return [(-x, -y, z) for x, y, z in cubes]

A = get_pyramid()

B = get_pyramid()
B = rotate_x_180(B)
B = rotate_z_90(B)

C = get_pyramid()
C = rotate_y_90(C)
C = rotate_z_180(C)

# Find translation for B
# We want B to interlock with A without overlap
# We can just brute force the offsets in a small range
valid_B_offsets = []
set_A = set(A)
for dx in range(-10, 10):
    for dy in range(-10, 10):
        for dz in range(-10, 10):
            offset_B = [(x+dx, y+dy, z+dz) for x, y, z in B]
            if len(set_A.intersection(offset_B)) == 0:
                # We want it to be adjacent, so bounding boxes overlap or it's tight
                valid_B_offsets.append((dx, dy, dz))

# To find the TIGHTEST fit, we want the bounding box of A U B to be minimal volume
best_B = None
min_vol_B = float('inf')
for dx, dy, dz in valid_B_offsets:
    offset_B = [(x+dx, y+dy, z+dz) for x, y, z in B]
    union = list(set_A) + offset_B
    xs = [c[0] for c in union]
    ys = [c[1] for c in union]
    zs = [c[2] for c in union]
    vol = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) * (max(zs) - min(zs) + 1)
    if vol < min_vol_B:
        min_vol_B = vol
        best_B = (dx, dy, dz)

print("Best B offset:", best_B)

offset_B_cubes = [(x+best_B[0], y+best_B[1], z+best_B[2]) for x, y, z in B]
set_AB = set_A.union(offset_B_cubes)

valid_C_offsets = []
for dx in range(-10, 10):
    for dy in range(-10, 10):
        for dz in range(-10, 10):
            offset_C = [(x+dx, y+dy, z+dz) for x, y, z in C]
            if len(set_AB.intersection(offset_C)) == 0:
                valid_C_offsets.append((dx, dy, dz))

best_C = None
min_vol_C = float('inf')
for dx, dy, dz in valid_C_offsets:
    offset_C = [(x+dx, y+dy, z+dz) for x, y, z in C]
    union = list(set_AB) + offset_C
    xs = [c[0] for c in union]
    ys = [c[1] for c in union]
    zs = [c[2] for c in union]
    vol = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) * (max(zs) - min(zs) + 1)
    if vol < min_vol_C:
        min_vol_C = vol
        best_C = (dx, dy, dz)

print("Best C offset:", best_C)

final_C_cubes = [(x+best_C[0], y+best_C[1], z+best_C[2]) for x, y, z in C]
set_ABC = set_AB.union(final_C_cubes)

xs = [c[0] for c in set_ABC]
ys = [c[1] for c in set_ABC]
zs = [c[2] for c in set_ABC]
print(f"Final shape size: X:{max(xs)-min(xs)+1}, Y:{max(ys)-min(ys)+1}, Z:{max(zs)-min(zs)+1}")
print(f"Total cubes: {len(set_ABC)}")
print(f"Volume of bounding box: {(max(xs)-min(xs)+1) * (max(ys)-min(ys)+1) * (max(zs)-min(zs)+1)}")
