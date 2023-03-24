import numpy as np
import matplotlib.pyplot as plt

# problem 1
# solving how much the water levels would drop if the qattara depression was filled with water

def water_level_drop():
    # volume of the qattara depression in km^3
    volume_qattara = 1213
    # surface area of water on earth in km^2
    surface_area = 3.619e8
    # how much would the water levels drop if the qattara depression was filled with water
    water_levels_drop = volume_qattara / surface_area
    # convert to from km to cm
    water_levels_drop *= 100000
    return water_levels_drop

print("The water levels would drop by", water_level_drop(), "cm if the qattara depression was filled with water.")

# problem 2
# load channel_data.txt file
import sys 
sys.path.append("/Users/ninapeuker/Desktop/General_Engineering/6th semester 2023/02526 Mathematical Modeling/02526 Code/MathModellingDTU/Qattara Depression")
path = "/Users/ninapeuker/Desktop/General_Engineering/6th semester 2023/02526 Mathematical Modeling/02526 Code/MathModellingDTU/Qattara Depression/"
data = np.loadtxt(path + "channel_data.txt")
#print(data)
latitude = data[:,0]
longitude = data[:,1]
height = data[:,2]

def distance_calculator():
    # create an empty array to store the distance between each point
    distance_array = [0]
    radius_earth = 6371
    # calculate the distance between each point such that there are 250 meter between each point
    for i in range(len(latitude)-1):
        # calculate the distance between each point using the haversine formula
        # convert latitude and longitude to radians
        lat1 = np.radians(latitude[i])
        lat2 = np.radians(latitude[i+1])
        lon1 = np.radians(longitude[i])
        lon2 = np.radians(longitude[i+1])
        # calculate the distance between each point
        distance = 2 * radius_earth * np.arcsin(np.sqrt(np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2))
        # add the distance to the distance array
        distance_array.append(distance_array[i] + distance)

    return distance_array

distances = distance_calculator()
print(distances)
print(len(height))

# create distance array for interpolation
dist_int = [0]
for i in range(int(distances[-1]/0.25)):
    dist_int.append(dist_int[-1]+0.25)

print(dist_int)


# interpolate the elevation data
height_interpolated = np.interp(dist_int, distances, height)
print(len(height_interpolated))

# convert interpolated elevation data to integers
height_interpolated = height_interpolated.astype(int)
#save the interpolated elevation data to a csv file with integers
np.savetxt("elevation_interpolated.txt", height_interpolated, fmt='%i', delimiter=",")


# plot distance vs elevation
plt.plot(dist_int, height_interpolated)
plt.xlabel("Distance (km)")
plt.ylabel("Elevation (m)")
plt.title("Distance vs Elevation")
plt.show()











