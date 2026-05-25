import numpy as np

N = 4
def get_pyramid():
    cubes = []
    for k in range(1, N + 1):
        for i in range(k):
            for j in range(k):
                cubes.append(np.array([j, -i, -k]))
    return cubes

A = get_pyramid()
def rot_x_180(v): return np.array([v[0], -v[1], -v[2]])
def rot_z_90(v): return np.array([-v[1], v[0], v[2]])
B = [rot_z_90(rot_x_180(v)) for v in get_pyramid()]

def rot_y_90(v): return np.array([v[2], v[1], -v[0]])
def rot_z_180(v): return np.array([-v[0], -v[1], v[2]])
C = [rot_z_180(rot_y_90(v)) for v in get_pyramid()]

best_B_offset = np.array([3, -4, -5])
best_C_offset = np.array([-1, -8, -1])

def get_bounds_center(cubes):
    xs = [c[0] for c in cubes]
    ys = [c[1] for c in cubes]
    zs = [c[2] for c in cubes]
    return np.array([(max(xs) + min(xs))/2.0, (max(ys) + min(ys))/2.0, (max(zs) + min(zs))/2.0])

center_A = get_bounds_center(A)
center_B = get_bounds_center(B)
center_C = get_bounds_center(C)

# We want B_shifted = B + best_B_offset
# B_shifted_center = center_B + best_B_offset
# The manim code does: B.target.shift(center_A - center_B + delta_B)
# So B_shifted_center = center_B + center_A - center_B + delta_B = center_A + delta_B
# Therefore, delta_B = best_B_offset + center_B - center_A

delta_B = best_B_offset + center_B - center_A
delta_C = best_C_offset + center_C - center_A

print("delta_B:", delta_B)
print("delta_C:", delta_C)
