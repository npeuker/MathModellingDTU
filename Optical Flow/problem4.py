import numpy as np
from PIL import Image
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from load_images import load_images

input("Enter video name: ")

path_to_video = r"C:\Users\miles\OneDrive\Desktop\Year 3\Math Modelling\Project 1 - Optical Flow\videos\vid1"

def load_images(path=path_to_video):
    # Array of images
    images = []
    for i in range(113):
        num = str(i)
        if i < 10:
            num = "0000" + num
        elif i>=10 and i < 100:
            num = "000" + num
        elif i>=100 and i < 1000:
            num = "00" + num
        imgi = np.array(Image.open(path +r"\vid1_frame_"+num+".jpg"))
        images.append(imgi)

    # Converting to greyscale
    grey_images = []
    for i in images:
        img = rgb2gray(i)
        grey_images.append(img)

    return grey_images


optical_flow_images = load_images()


# Determining the dimensions of the images

print(len(optical_flow_images))
print(len(optical_flow_images[0]))
print(len(optical_flow_images[0][0]))




# Perform optical flow on the images
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


G_x, G_y, G_t = gaussian_gradients(optical_flow_images, 0.4)

# NxN  window
N = 5 # Must be odd and > 1!
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


# Lucas-Kanade method and Linear Least Squares

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


# Function to calculate the magnitude of the optical flow
def calc_mag(u):
    return np.sqrt(u[0]**2 + u[1]**2)

min_mag = 100
max_mag = 2000

# Iterate over all images
for l in range(70, len(optical_flow_images)): 
    # Iterate over all pixels
    origin_x, origin_y = [],[]
    dir_x, dir_y = [],[]
    fig, ax = plt.subplots()
    for i in range(0, 700, 10):
        for j in range(0, 700, 10):
            ax.imshow(optical_flow_images[l], cmap=plt.cm.gray)
            ax.set_title("Image " + str(l))
            # Calculate the optical flow for the pixel
            V_x, V_y, V_t = retrieve_gradients((i, j), m, optical_flow_images, l)
            A = make_A(V_x, V_y)
            u = calc_optical_flow(A, V_t)
            # If the magnitude of the optical flow is too small, ignore it
            if calc_mag(u) > min_mag and calc_mag(u) < max_mag:
                print("Adding vector + " + str(u) + " at " + str((i, j)))
                origin_x.append(j)
                origin_y.append(i)
                dir_x.append(u[0])
                dir_y.append(u[1])
    title = ""
    if l < 10:
        title = "0"+str(l+1)+"image.png"
    else:
        title = str(l)+"image.png"
    print("Saving image: " + title)
    ax.quiver(origin_x, origin_y, dir_x, dir_y, color='r')
    ax.set_title(str(l+1))
    fig.savefig(r"C:/Users/miles/OneDrive/Desktop/Year 3/Math Modelling/Project 1 - Optical Flow/Optical Flow/testimages/vid1/"+title)
    plt.close(fig)
    exit()
    
    
                


            