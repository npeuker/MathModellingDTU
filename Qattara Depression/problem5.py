from problem1and2 import *
from problem3and4 import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



# problem 5
# load a dataframe from the csv file
import pandas as pd
df = pd.read_csv("nukeDemo5.csv", header=None)
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
print("Number of nukes needed for the optimzed model", sum(x))

nukes_optimized = [0 for i in range(len(x))]

channelheight_optimized = [0 for i in range(len(x))]
for i in range(len(x)):
    channelheight_optimized[i] = height_interpolated[i] - R_optimized[i]

for i in range(len(x)):
    if x[i] == 1:
        nukes_optimized[i] = channelheight_optimized[i]
    else:
        continue

print(nukes_optimized)

for i in range(len(nukes_optimized)):
    if nukes_optimized[i] == 0:
        nukes_optimized[i] = np.nan
    else:
        continue

plt.plot(distances, channelheight_optimized,label = "Channel Height Optimized Model")
plt.scatter(distances, nukes_optimized,label = "Nuclear bombs" , color='red')
plt.xlabel("Distance (m)")
plt.ylabel("Channel Height (m)")
plt.title("Channel Height for model where two bombs not are next to each other")
plt.legend()
plt.show()
