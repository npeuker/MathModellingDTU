
"""
Created on Tue Sep 29 09:16:42 2020

@author: bossema
"""
import numpy as np
from plank_phantom import phantom_plank
import line_geometry as lg
import numpy as np
from flexdata import display
from flexdata import data
import matplotlib.pyplot as plt

variable = 'angles'
ringwidths = np.array([1.0])

angles = np.array([0, 8,15])
save_path = 'test-phantoms'

pix_size = 0.05

phantom_size = (20,100,50) #millimeters: height, depth, width

angle = 0
angle = np.deg2rad(angle)


for j, ring_width in enumerate(ringwidths):
    print(f"j {j}, Ring Width: {ring_width}")
    for i in angles: #change this line! 
        name = f'phantom_width{j+1}{variable}{i}'

        #create phantom with tree ring size
        
        P = phantom_plank(phantom_size, angle = np.deg2rad(i), p = pix_size, ring_width = ring_width, gaussian_blurr = 2).transpose([0,2,1])
        
        image = P[:,0,:]
        # plt.imsave(save_path + name+'.png', image, vmin = -1, vmax =2, cmap = 'gray')
        display.slice(P, title = 'Phantom', dim = 1, index = 0)

        plt.imshow(image, cmap="gray") # Should do the same as above 
        plt.show()
