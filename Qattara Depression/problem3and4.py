import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from problem1and2 import height_interpolated, distances

# problem 3
# load a dataframe from the csv file
import pandas as pd
df = pd.read_csv("nukeDemo.csv", header=None)
# extract the data from the dataframe
data = df.values
# print(data)
myModel = data[:,0][1:]
x = data[:,1][1:]
# convert x to floats
x = x.astype(float)
x = x.astype(int)

R_optimized = data[:,2][1:]
R_optimized = R_optimized.astype(float)
R_optimized = R_optimized.astype(int)

# Number of nukes needed


Dist_H = [0 for i in range(len(x))]
Height_H = [0 for i in range(len(x))]
# print("Number of nukes needed not smooth model:", sum(x))
for i in range(len(x)):
    if x[i] == 1:
        Dist_H[i] = distances[i]
        Height_H[i] = height_interpolated[i]
    else:
        continue

        
# problem 4
# load newNukeDemo.csv file
df1 = pd.read_csv("newNukeDemo.csv", header=None)
# extract the data from the dataframe
data1 = df1.values

myModel1 = data1[:,0][1:]
x1 = data1[:,1][1:]
# convert x to floats
x1 = x1.astype(float)
x1 = x1.astype(int)

R1 = data1[:,2][1:]
R1 = R1.astype(float)
R1 = R1.astype(int)

# Number of nukes needed
# print("Number of nukes needed for smooth model:", sum(x1))
Dist_H1 = [0 for i in range(len(x1))]
Height_H1 = [0 for i in range(len(x1))]
for i in range(len(x1)):
    if x1[i] == 1:
        Dist_H1[i] = distances[i]
        Height_H1[i] = height_interpolated[i]
    else:
        continue

channelheight = [0 for i in range(len(x))]
channelheight1 = [0 for i in range(len(x1))]
for i in range(len(x)):
    channelheight[i] = height_interpolated[i] - R_optimized[i]
    channelheight1[i] = height_interpolated[i] - R1[i]

# print("Channel depth not smooth model:", channelheight)
# print("Channel depth smooth model:", channelheight1)

# where nukes are placed in the channel
nukes_notSmooth = [0 for i in range(len(x))]
nukes_smooth = [0 for i in range(len(x1))]

for i in range(len(x)):
    if x[i] == 1:
        nukes_notSmooth[i] = channelheight[i]
    else:
        continue

for i in range(len(x1)):
    if x1[i] == 1:
        nukes_smooth[i] = channelheight1[i]
    else:
        continue

for i in range(len(nukes_notSmooth)):
    if nukes_notSmooth[i] == 0:
        nukes_notSmooth[i] = np.nan
    else:
        continue

for i in range(len(nukes_smooth)):
    if nukes_smooth[i] == 0:
        nukes_smooth[i] = np.nan
    else:
        continue

# print("Placement of nukes not smooth model:", nukes_notSmooth)
# print("Placement of nukes smooth model:", nukes_smooth)

# make distances the same length as x
distances = distances[:len(x)]

# plot the dept of the channel for the not smooth model with placement of nukes
# plt.plot(distances, channelheight, label="Channel depth not smooth model")
# plt.scatter(distances, nukes_notSmooth, label="Placement of nukes not smooth model", color="red")
# plt.xlabel("Distance (m)")
# plt.ylabel("Channel depth (m)")
# plt.legend()
# plt.show()

# plot the dept of the channel for the smooth model with placement of nukes
# plt.plot(distances, channelheight1, label="Channel depth smooth model")
# plt.scatter(distances, nukes_smooth, label="Placement of nukes smooth model", color="red")
# plt.xlabel("Distance (m)")
# plt.ylabel("Channel depth (m)")
# plt.legend()
# plt.show()








