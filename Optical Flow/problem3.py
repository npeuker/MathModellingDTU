import numpy as np
from PIL import Image
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from scipy import ndimage
from load_images import load_images


grey_images = load_images()


# Checks if a pixel is in the frame - Used for retrieving gradients in the window

def pixel_in_frame(i, j, grey_images):
    # Returns true if the pixel is in the frame
    if i >= 0 and i < len(grey_images[0]) and j >= 0 and j < len(grey_images[0][0]):
        return True
    else:
        return False

# Using Gaussian filter to calculate the image gradients

def gaussian_gradients(grey_images, sigma):
    G_3D_x = ndimage.gaussian_filter(grey_images, sigma=sigma, order=[1,0,0])
    G_3D_y = ndimage.gaussian_filter(grey_images, sigma=sigma, order=[0,1,0])
    G_3D_t = ndimage.gaussian_filter(grey_images, sigma=sigma, order=[0,0,1])

    return G_3D_x, G_3D_y, G_3D_t


G_x, G_y, G_t = gaussian_gradients(grey_images, 1)

# Pixel of arbitrary location - On ball
p = (115, 50)

# NxN  window
N = 3 # Must be odd and > 1!
m = int((N-1)/2)

# Retrieving values for gradients in the window around the pixel
def retrieve_gradients(p, m, grey_images, image_num, d_x=G_x, d_y=G_y, d_t=G_t):
    V_x = []
    V_y = []
    V_t = []
    for i in range(-m, m+1):
        for j in range(-m, m+1):
            if pixel_in_frame(p[0]+i, p[1]+j, grey_images):
                V_x.append(d_x[image_num][p[0]+i][p[1]+j])
                V_y.append(d_y[image_num][p[0]+i][p[1]+j])
                V_t.append(d_t[image_num][p[0]+i][p[1]+j])
    return V_x, V_y, V_t

V_x, V_y, V_t = retrieve_gradients(p, m, grey_images, 0, G_x, G_y, G_t)

# displaying values of gradients in the window
# print("V_x = ", V_x)
# print("V_y = ", V_y)
# print("V_t = ", V_t)

# Calculating the optical flow - Using Lucas-Kanade method and Linear Least Squares

# Creating the A matrix
def make_A(V_x, V_y):
    A = []
    for i in range(len(V_x)):
        A.append([V_x[i], V_y[i]])
    return np.array(A)

# Calculating the optical flow
def calc_optical_flow(A, V_t):
    V_t = -1*np.array(V_t)
    u = np.linalg.lstsq(A, V_t, rcond=None)[0]
    return u

A = make_A(V_x, V_y)
u = calc_optical_flow(A, V_t)

# Displaying the optical flow
# plt.imshow(grey_images[0], cmap=plt.cm.gray)
# plt.title("Image 1")
# plt.quiver(p[1], p[0], u[0], u[1], color='r')
# plt.show()

# Doing the same for n images

# for i in range(10): 
#     V_x, V_y, V_t = retrieve_gradients(p, m, grey_images, i)
#     A = make_A(V_x, V_y)
#     u = calc_optical_flow(A, V_t)
#     plt.imshow(grey_images[i], cmap=plt.cm.gray)
#     plt.title("Image " + str(i))
#     plt.quiver(p[1], p[0], u[0], u[1], color='r')
#     plt.show()



# 3.2 - Applying above to all frames
# (3.3) Also ignoring displacement vectors that are too small

# Function to calculate the magnitude of the optical flow
def calc_mag(u):
    return np.sqrt(u[0]**2 + u[1]**2)

min_mag = 4

# Iterate over all images
for l in range(len(grey_images)): # Ignore first image
    # Iterate over all pixels
    origin_x, origin_y = [],[]
    dir_x, dir_y = [],[]
    fig, ax = plt.subplots()
    for i in range(0, 256, 10):
        for j in range(0, 256, 10):
            ax.imshow(grey_images[l], cmap=plt.cm.gray)
            ax.set_title("Image " + str(l))
            # Calculate the optical flow for the pixel
            V_x, V_y, V_t = retrieve_gradients((i, j), m, grey_images, l)
            A = make_A(V_x, V_y)
            u = calc_optical_flow(A, V_t)
            # If the magnitude of the optical flow is too small, ignore it
            if calc_mag(u) > min_mag:
                print("Adding vector + " + str(u) + " at " + str((i, j)))
                origin_x.append(j)
                origin_y.append(i)
                dir_x.append(u[0])
                dir_y.append(u[1])

    ax.quiver(origin_x, origin_y, dir_x, dir_y, color='r')
    plt.show()
    exit() # Only show first image
                