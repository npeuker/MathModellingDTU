from plank_phantom import phantom_plank
import numpy as np
import matplotlib.pyplot as plt
import time

def gen_plank(size=500, ring_width=30.0, blur=5, angle=0):
    plank_size = (size, size, size)
    v0 = ((-1/2)*plank_size[1], (1/2)*plank_size[0],(1/2)*plank_size[2])
    angle = np.deg2rad(angle)
    pix_size = 1
    P = phantom_plank(plank_size, angle = angle, p = pix_size, ring_width = ring_width, gaussian_blurr=blur)
    return P

def add_shot(slice, x, y, size, metal):
    metal_to_AC = {"lead": 30.32, "steel": 7.938406}
    if x+size > slice.shape[1] or y+size > slice.shape[0]:
        raise Exception(f"Bullet of specified dimensions will be out of bounds.\nplank size: {slice.shape}") 
    slice[y:y+size, x:x+size] = metal_to_AC[metal]
    return slice
    

def get_slices(P):
    return [P[:, :, 0], P[:, :, 100], P[:, :, 200], P[:, :, 300],P[:, :, 400]]
    
folder = "validation-data"

t1 = time.time()
# First plank

# subfolder = "/plank1/"
# ring_width1 = 30
# angle1 = 0
# blur1 = 5
# plank = gen_plank(ring_width=ring_width1, blur=blur1, angle=angle1)
# slices=get_slices(plank)

# for i in [0, 1, 2, 3, 4]:
#     plt.imsave(folder+subfolder+f"slice{i}.png", slices[i])


# Second plank

# subfolder = "/plank2/"
# ring_width2 = 40
# angle2 = 2
# blur2 = 3
# plank = gen_plank(ring_width=ring_width2, blur=blur2, angle=angle2)
# slices=get_slices(plank)

# for i in [0, 1, 2, 3, 4]:
#     plt.imsave(folder+subfolder+f"slice{i}.png", slices[i])


# Third plank

# subfolder = "/plank3/"
# ring_width3 = 50
# angle3 = 0
# blur3 = 2
# plank = gen_plank(ring_width=ring_width3, blur=blur3, angle=angle3)
# slices=get_slices(plank)

# for i in [0, 1, 2, 3, 4]:
#     plt.imsave(folder+subfolder+f"slice{i}.png", slices[i])


# Fourth/final plank

subfolder = "/plank4/"
ring_width4 = 30
angle4 = 5
blur4 = 5
plank = gen_plank(ring_width=ring_width4, blur=blur4, angle=angle4)
slices=get_slices(plank)

for i in [0, 1, 2, 3, 4]:
    plt.imsave(folder+subfolder+f"slice{i}.png", slices[i])



t2 = time.time()

print(f"Time required to save images: {t2-t1}s")