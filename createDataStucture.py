import pickle
from math import pi, acos, sin, cos

fileNodes = open("rrNodes.txt", 'r')
latlong = {}
for line in fileNodes.readlines():
    ver, lat, longti = line.strip().split(' ')
    latlong[ver] = (lat, longti)

mylatlongFile = open("latlong", "wb")
pickle.dump(latlong, mylatlongFile)


def calcd(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


data = {}
fileEdges = open("rrEdges.txt", 'r')
for line in fileEdges.readlines():
    ver1, ver2 = line.strip().split(' ')
    GD = calcd(latlong[ver1][0], latlong[ver1][1], latlong[ver2][0], latlong[ver2][1])
    if ver1 not in data:
        data[ver1] = {ver2: GD}
    else:
        data[ver1][ver2] = GD
    if ver2 not in data:
        data[ver2] = {ver1: GD}
    else:
        data[ver2][ver1] = GD

fileCities = open("rrCities.txt", 'r')
cities = {}
for line in fileCities.readlines():
    index, cityName = line.strip().split(' ', 1)
    cities[cityName] = index
print(cities)

myCityFile = open("cities", "wb")
pickle.dump(cities, myCityFile)
myFile = open("data", "wb")
pickle.dump(data, myFile)
