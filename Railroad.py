import pickle
from timeit import default_timer as timer
import heapq
import tkinter as tk
from math import pi, acos, sin, cos

myFile = open("data", "rb")
data = pickle.load(myFile)
myEdges = open("cities", "rb")
cities = pickle.load(myEdges)
thelatlongs = open("latlong", "rb")
myLatLong = pickle.load(thelatlongs)


class RailNode():
    def __init__(self, theid, distance, greatcircle, childrens):
        self.myID = theid
        self.realdist = distance
        self.GC = greatcircle
        self.children = childrens

    def __lt__(self, other):
        return (self.realdist + self.GC) - (other.realdist + other.GC)


def calcd(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions
    if (y1 == y2 and x1 == x2):
        return 0
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


def AStar(start, goal):
    startVer = cities[start]
    goalVer = cities[goal]
    latF, longF = myLatLong[goalVer]
    latlong = myLatLong[startVer]
    rootNode = RailNode(startVer, 0, calcd(latlong[0], latlong[1], latF, longF), data[startVer])
    fringe = list()
    seen = set()
    heapq.heappush(fringe, rootNode)
    while fringe:
        node = heapq.heappop(fringe)
        if node.myID in seen: continue
        seen.add(node.myID)
        if node.myID == goalVer:
            print(node.realdist)
            return
        children = node.children
        for key in children:
            childLat, childLong = myLatLong[key]
            greatDistance = calcd(childLat, childLong, latF, longF)
            childNode = RailNode(key, node.realdist + children[key], greatDistance, data[key])
            if key not in seen:
                heapq.heappush(fringe, childNode)


def alsoStar(start,goal):
	startVer = cities[start]
	goalVer = cities[goal]
	latF, longF = myLatLong[goalVer]
	latlong = myLatLong[startVer]
	fringe = list()
	seen = set()
	heapq.heappush(fringe, (0 + calcd(latlong[0], latlong[1], latF, longF), startVer,0, calcd(latlong[0],latlong[1],latF,longF),data[startVer]))
	while fringe:
		f, vertex, realdist, greatDist, children = heapq.heappop(fringe)
		if vertex in seen: continue
		seen.add(vertex)
		if vertex == goalVer:
			print(realdist)
			return
		for key in children:
			childLat, childLong = myLatLong[key]
			greatDistance = calcd(childLat, childLong, latF, longF)
			newRealDist = realdist + data[vertex][key]
			if key not in seen:
				heapq.heappush(fringe, (newRealDist + greatDistance, key, realdist + data[vertex][key], greatDistance, data[key]))

alsoStar("Washington DC", "Merida")
latInc = 600/ 46.16
longInc = 1000 / 70.333
maximumLat = 60.846
minimumLat = 14.686
maximumLong = -60.0240
minimumLong = -130.357
master = tk.Tk()

def findLatLong(lat1,long1):
    return ((maximumLat - float(lat1)) * latInc, (float(long1) - minimumLong) * longInc)


def drawMap():
    w = tk.Canvas(master, width = 1000, height = 600)
    w.pack()
    for children in data:
        for edge in data[children]:
            node1 = myLatLong[children]
            node2 = myLatLong[edge]
            correctNum1 = findLatLong(node1[0], node1[1])
            correctNum2 = findLatLong(node2[0], node2[1])
            w.create_line(correctNum2[1], correctNum2[0], correctNum1[1], correctNum1[0],fill = "red")
    w.update()
    tk.mainloop()




drawMap()



maxLat = -1000
minLat = 1000
maxLong = -1000
minLong = 1000
for key in myLatLong:
	lat, longt = myLatLong[key]
	lat = float(lat)
	longt = float(longt)
	if maxLat < lat:
		maxLat = lat
	if minLat > lat:
		minLat =lat
	if maxLong < longt:
		maxLong = longt
	if minLong > longt:
		minLong = longt
print("Lat Range " + str(maxLat - minLat) + " Long Range " + str(maxLong - minLong))
print(str(maxLat) + " " + str(minLat) + " " + str(maxLong) + " " + str(minLong))




