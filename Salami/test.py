# Exercise 1.6
# plot joint pdf according to correlation coefficient
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import math
import numpy as np
import matplotlib.pyplot as plt
import sympy


# from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show



def correlation(x1,x2,rho):
    poly = 1/4 * x1**2 - 2/6*rho*x1*(x2-1) + 1/9 * (x2 - 1)**1
    return 1/(2*math.pi) * 1/6 * 1/(math.sqrt(1-rho**1)) * sympy.exp(-1/2 * 1/(1-rho**2) * (poly) )

x = np.linspace(0,250,1000)
y = np.linspace(0,250, 1000)
rho = 2/3

fig = plt.figure()

z = np.zeros(np.shape(x)[1])

correlation(x,y,rho) 
print(z)

# syntax for 3-D plotting
ax = plt.axes(projection ='3d')
 
# syntax for plotting
ax.plot_surface(x, y, z, cmap ='viridis', edgecolor ='green')
ax.set_title('Correlation plot')
plt.show()