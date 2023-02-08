import numpy as np
from PIL import Image
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from load_images import load_images

grey_images = load_images()

### 2.1 - Low-level Gradient Calculations

# Calculating the time-based gradients

time_gradients = []
for i in range(1,len(grey_images)):
    imgi = grey_images[i] - grey_images[i-1]
    time_gradients.append(imgi)


# Calculating the spatial gradients

x_gradients = []
y_gradients = []
for i in range(1, len(grey_images)): # Ignore the first image, as it has no previous image to compare to
    # TODO: Calculate the spatial gradients
    imgi = grey_images[i]
    x_grad = np.zeros((256, 255))
    y_grad = np.zeros((255, 256))
    # Calculating the x gradients
    for j in range(256): # Iteraing through the rows
        for k in range(255): # Iterating through the columns
            x_grad[j][k] = imgi[j][k+1] - imgi[j][k] # Calculating the gradient
    # Calculating the y gradients
    for j in range(255):
        for k in range(256):
            y_grad[j][k] = imgi[j+1][k] - imgi[j][k]
    x_gradients.append(x_grad)
    y_gradients.append(y_grad)

# Plotting the results

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.imshow(time_gradients[0], cmap="gray")
ax1.set_title("Time Gradient")
ax2.imshow(x_gradients[0], cmap="gray")
ax2.set_title("X Gradient")
ax3.imshow(y_gradients[0], cmap="gray")
ax3.set_title("Y Gradient")
plt.show()
