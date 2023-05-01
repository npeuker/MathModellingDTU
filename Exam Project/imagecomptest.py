import numpy as np
import matplotlib.pyplot as plt
from create_test_image import new_image
from paralleltomo import paralleltomo
from scipy.ndimage import zoom


im = new_image(500)

resized_im = zoom(im, (0.1, 0.1), order=1) # Using Bilinear Interpolation
[A,theta,p,d] = paralleltomo(50)
x = np.ravel(resized_im)

# Simulating forward projection

def forwardProj(A, x):
    return np.matmul(A, x)

def solveForX(A, b):
    return np.linalg.lstsq(A, b)[0]

b = forwardProj(A, x)
x_solved = solveForX(A, b)

new_im = np.resize(x_solved, (50,50))

plt.imshow(im)
plt.title("Original Image")
plt.show()


plt.imshow(resized_im)
plt.title("Original Image (resized)")
plt.show()

plt.imshow(new_im)
plt.title("Recreated Image")
plt.show()


mse = np.mean(np.square(new_im-resized_im))


print(f"Mean Square Difference between image and reconstructed image: {mse}")