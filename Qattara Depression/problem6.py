from problem1and2 import *
from problem3and4 import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# problem 6
# load a dataframe from the csv file
import pandas as pd
df = pd.read_csv("nukeDemo6.csv", header=None)
# extract the data from the dataframe
data = df.values
# print(data)
myModel = data[:,0][1:]
x = data[:,1][1:]
# convert x to floats
x = x.astype(float)
x = x.astype(int)

amount_of_dirt_removed = data[:,2][1:]
amount_of_dirt_removed = amount_of_dirt_removed.astype(float)
amount_of_dirt_removed = amount_of_dirt_removed.astype(int)

# Number of nukes needed
print("Number of nukes needed for the optimzed model", sum(x))

nukes_optimized = [0 for i in range(len(x))]

channelheight_optimized = [0 for i in range(len(x))]
for i in range(len(x)):
    channelheight_optimized[i] = height_interpolated[i] - amount_of_dirt_removed[i]

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

plt.plot(distances, channelheight_optimized,label = "Channel depth model with setting")
plt.scatter(distances, nukes_optimized,label = "Nuclear bombs" , color='red')
plt.xlabel("Distance (m)")
plt.ylabel("Channel depth (m)")
plt.title("Channel depth for model with different settings")
plt.legend()
plt.show()
