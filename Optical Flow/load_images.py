import numpy as np
from PIL import Image
from skimage.color import rgb2gray

def load_images(path=r"C:\Users\miles\OneDrive\Desktop\Year 3\Math Modelling\Project 1 - Optical Flow\toyProblem_F22"):
    # Array of the 64 images
    images = []
    for i in range(1, 65):
        num = str(i)
        if i < 10:
            num = "0" + num
        imgi = np.array(Image.open(path + r"\frame_"+num+".png"))
        images.append(imgi)


    # Converting to greyscale
    grey_images = []
    for i in range(len(images)):
        imgi = rgb2gray(images[i])
        grey_images.append(imgi)
    return grey_images

