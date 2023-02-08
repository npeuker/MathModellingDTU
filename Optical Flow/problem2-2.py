import numpy as np
from PIL import Image
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from load_images import load_images

grey_images = load_images()

### 2.2 - Simple Gradient Filters

# Using Prewitt filter

prewitt_x = []
prewitt_y = []

for i in range(len(grey_images)):
    # Prewitt filter for x
    prewitt_x.append(ndimage.prewitt(grey_images[i], axis=1))
    # Prewitt filter for y
    prewitt_y.append(ndimage.prewitt(grey_images[i], axis=0))

# Using Sobel filter

sobel_x = []
sobel_y = []

for i in range(len(grey_images)):
    # Sobel filter for x
    sobel_x.append(ndimage.sobel(grey_images[i], axis=1))
    # Sobel filter for y
    sobel_y.append(ndimage.sobel(grey_images[i], axis=0))

# Plotting the results

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
ax1.imshow(prewitt_x[0], cmap="gray")
ax1.set_title("Prewitt X")
ax2.imshow(prewitt_y[0], cmap="gray")
ax2.set_title("Prewitt Y")
ax3.imshow(sobel_x[0], cmap="gray")
ax3.set_title("Sobel X")
ax4.imshow(sobel_y[0], cmap="gray")
ax4.set_title("Sobel Y")
plt.show()
