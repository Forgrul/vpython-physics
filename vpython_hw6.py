import numpy as np

R = 0.12
r = 0.06
I = 1
m = 500
n = 500
N1 = N2 = 1
miu = 4 * np.pi * 1E-7
magnetic_flux1 = 0
magnetic_flux2 = 0

thetas = np.linspace(0, 2*np.pi, n, endpoint=False)
big_ring_ds_pos = np.zeros((n, 3))
big_ring_ds_pos[:,0] = R*np.cos(thetas)
big_ring_ds_pos[:,1] = R*np.sin(thetas)
small_ring_ds_pos = np.zeros((n, 3))
small_ring_ds_pos[:,0] = r*np.cos(thetas)
small_ring_ds_pos[:,1] = r*np.sin(thetas)
small_ring_ds_pos[:,2] = 0.1

big_ring_pos = np.zeros((m, 3))
big_ring_pos[:, 0] = np.linspace(0, R, m, endpoint=False)
small_ring_pos = np.zeros((m, 3))
small_ring_pos[:, 2] = 0.1
small_ring_pos[:, 0] = np.linspace(0, r, m, endpoint=False)

def distance(pos_a, pos_b):
    return np.linalg.norm(pos_a - pos_b)

ds1 = (2*np.pi*R) / n
ds2 = (2*np.pi*r) / n
big_ring_width = R / m
small_ring_width = r / m
for i in range(m):
    Bz1 = 0
    Bz2 = 0
    for j in range(n):
        vec_r1 = small_ring_pos[i] - big_ring_ds_pos[j]
        vec_ds1 = big_ring_ds_pos[j] - big_ring_ds_pos[(j - 1) % n]
        dist = distance(small_ring_pos[i], big_ring_ds_pos[j])
        B1 = miu * I / (4 * np.pi) * np.cross(vec_ds1, vec_r1) / dist**3
        Bz1 += np.dot(B1, [0, 0, 1])

        vec_r2 = big_ring_pos[i] - small_ring_ds_pos[j]
        vec_ds2 = small_ring_ds_pos[j] - small_ring_ds_pos[(j - 1) % n]
        dist = distance(big_ring_pos[i], small_ring_ds_pos[j])
        B2 = miu * I / (4 * np.pi) * np.cross(vec_ds2, vec_r2) / dist**3
        Bz2 += np.dot(B2, [0, 0, 1])
    
    area1 = (np.pi * small_ring_pos[i,0]**2) - (np.pi * (small_ring_pos[i,0] - small_ring_width)**2)
    magnetic_flux1 += Bz1 * area1

    area2 = (np.pi * big_ring_pos[i,0]**2) - (np.pi * (big_ring_pos[i,0] - big_ring_width)**2)
    magnetic_flux2 += Bz2 * area2

M1 = magnetic_flux1 * N1 / I
M2 = magnetic_flux2 * N2 / I

print(M1)
print(M2)