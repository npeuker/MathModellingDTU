import numpy as np
import random
import matplotlib.pyplot as plt

def create_new_im(size):
    attenuation_wood = 4.2848231320000005
    attenuation_steel = 395.44319
    attenuation_lead = 130.6
    image = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            if random.random() < 0.0008:
                image[i,j] = attenuation_lead
            elif random.random() < 0.001:
                image[i,j] = attenuation_steel
            else:
                image[i,j] = attenuation_wood

    return image

image = create_new_im(50)

plt.imshow(image)
plt.show()