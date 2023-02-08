import numpy as np
from PIL import Image
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from load_images import load_images

grey_images = load_images()

### 2.3 - Gaussian Gradient Filters

sigma = 1

# 1D Gaussian filter

G_x = []
G_y = []
print("Smoothing images with 1D Gaussian filter...")

for i in range(len(grey_images)):
    # Gaussian filter for x and y
    G_x.append(ndimage.gaussian_filter1d(grey_images[i], sigma=sigma,axis=1))
    G_y.append(ndimage.gaussian_filter1d(grey_images[i], sigma=sigma, axis=0))

# Displaying smoothed images
print("Displaying smoothed images")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.imshow(G_x[0], cmap=plt.cm.gray)
ax1.set_title("Gaussian x")
ax2.imshow(G_y[0], cmap=plt.cm.gray)
ax2.set_title("Gaussian y")
plt.show()

# Finding gradients of 1D smoothed images 
G_x_x=[]
G_y_y=[]
for i in range(len(G_x)):
    imgx = G_x[i]
    imgy = G_y[i]
    G_x_dx = np.zeros((256, 255))
    G_y_dy = np.zeros((255, 256))
    # Calculating the x gradients
    for j in range(256):
        for k in range(255):
            G_x_dx[j][k] = imgx[j][k+1] - imgx[j][k]
    # Calculating the y gradients
    for j in range(255):
        for k in range(256):
            G_y_dy[j][k] = imgy[j+1][k] - imgy[j][k]
    G_x_x.append(G_x_dx)
    G_y_y.append(G_y_dy)

# Plotting the results
print("Plotting the results")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.imshow(G_x_x[0], cmap=plt.cm.gray)
ax1.set_title("1D Gaussian x gradient")
ax2.imshow(G_y_y[0], cmap=plt.cm.gray)
ax2.set_title("1D Gaussian y gradient")
plt.show()

# Applying the gaussian filter in 3D and comparing to consecutive 1D filters

G_3D = ndimage.gaussian_filter(grey_images, sigma=sigma)

G_consec = (ndimage.gaussian_filter1d(ndimage.gaussian_filter1d(ndimage.gaussian_filter1d(grey_images, sigma=sigma, axis=2), sigma=sigma,axis=1), sigma=sigma, axis=0))
    
# Comparing the results

print("Comparing the results of consecutive 1D filters and 3D filter")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.imshow(G_3D[0], cmap=plt.cm.gray)
ax1.set_title("3D Gaussian")
ax2.imshow(G_consec[0], cmap=plt.cm.gray)
ax2.set_title("Consecutive 1D Gaussian")
plt.show()

# Calculating image gradient in one step, using the derivative of the gaussian filter 

G_3D_x = ndimage.gaussian_filter(grey_images, sigma=sigma, order=[1,0,0])
G_3D_y = ndimage.gaussian_filter(grey_images, sigma=sigma, order=[0,1,0])
G_3D_t = ndimage.gaussian_filter(grey_images, sigma=sigma, order=[0,0,1])

# Comparing the results to that of sobel filter applied to smoothed images

sobel_x = []
sobel_y = []

for i in range(len(G_3D)):
    # Sobel filter for x
    sobel_x.append(ndimage.sobel(G_3D[i], axis=1))
    # Sobel filter for y
    sobel_y.append(ndimage.sobel(G_3D[i], axis=0))

print("Comparing the results of the 3D Gaussian filter and the Sobel filter applied to smoothed images")
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 5))
ax1.imshow(G_3D_x[0], cmap=plt.cm.gray)
ax1.set_title("3D Gaussian x")
ax2.imshow(G_3D_y[0], cmap=plt.cm.gray)
ax2.set_title("3D Gaussian y")
ax3.imshow(sobel_x[0], cmap=plt.cm.gray)
ax3.set_title("Sobel x")
ax4.imshow(sobel_y[0], cmap=plt.cm.gray)
ax4.set_title("Sobel y")
plt.show()


