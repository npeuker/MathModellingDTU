import numpy as np
import random
import matplotlib.pyplot as plt

def new_image(size):
    attenuation_wood = 4.2848231320000005
    attenuation_steel = 395.44319
    attenuation_lead = 130.6
    image = np.zeros((size,size))
    resize = int(size/100)
    for i in range(resize,size-resize, resize):
        for j in range(resize, size-resize, resize):
            if random.random() < 0.00015:
                image[i:i+resize,j:j+resize] = attenuation_lead
            elif random.random() < 0.00015:
                image[i:i+resize,j:j+resize] = attenuation_steel
            else:
                image[i][j] = attenuation_wood
    return image

# create 10 images
# size = 500
# for i in range(3):
#     a = new_image(size)
#     plt.imshow(a)
#     plt.show()
#     np.save(f'Exam Project/test images without noise/new_test_image{i}', a)
