# Siddharth Shah
# Yellow-Cities, Red-OpenSet, Blue-ClosedSet, Green-ShortestPath
import sys, tkinter
from math import pi, acos, sin, cos

def readNodes(fileName, nodeToPos):
    nodes = open(fileName, "r").read().splitlines()
    for node in nodes:
        space1 = node.index(" ")
        space2 = node.index(" ", space1+1)
        nodeToPos[node[:space1]] = (float(node[space1+1:space2]), float(node[space2+1:]))

def readEdges(fileName, nodeToNodes):
    edges = open(fileName, "r").read().splitlines()
    for edge in edges:
        space = edge.index(" ")
        if edge[:space] not in nodeToNodes: nodeToNodes[edge[:space]] = []
        nodeToNodes[edge[:space]].append(edge[space+1:])
        if edge[space+1:] not in nodeToNodes: nodeToNodes[edge[space+1:]] = []
        nodeToNodes[edge[space+1:]].append(edge[:space])
        addEdge("grey", edge[:space], edge[space+1:], 1)

def readCities(fileName, nodeToCity, cityToNode):
    cities = open(fileName, "r").read().splitlines()
    for city in cities:
        space = city.index(" ")
        nodeToCity[city[:space]] = city[space+1:]
        cityToNode[city[space+1:]] = city[:space]

def addPoint(color, node): #Takes Node ID
    pos = nodeToPos[node]
    y1 = convertLat(pos[0])
    x1 = convertLon(pos[1])
    canvas.create_oval(x1, y1, x1+10, y1+10, fill = color)

def addEdge(color, node1, node2, width):  #Takes Node ID
    pos1 = nodeToPos[node1]
    pos2 = nodeToPos[node2]
    y1 = convertLat(pos1[0])+5 # For Middle of Node
    x1 = convertLon(pos1[1])+5
    y2 = convertLat(pos2[0])+5
    x2 = convertLon(pos2[1])+5
    canvas.create_line(x1, y1, x2, y2, fill = color, width = width)

def convertLat(value): #Make Lowest 0, Scale 0-480, center via 10, and invert
    return 500 - ((value-14.68673)*480/46.16009 + 10)

def convertLon(value): #Make Lowest 0, Scale 0-960, center via 20
    return (value+130.35722)*960/70.33319 + 20

def determineCities(words):
    for i in range(1, len(words)):
        cities = (" ".join(words[:i]), " ".join(words[i:]))
        if cities[0] in cityToNode and cities[1] in cityToNode: return cities
    return("", "") #Cities Not Valid

def shortestPath(root, goal):
    if root == goal: return [root]
    openSet = [(h(root, goal), root, "", 0)]
    closedSet = {}
    count = 1
    while openSet:
        if not count%SPEED: canvas.update() 
        f, pzl, parent, dist = openSet.pop(0)
        if parent: addEdge("blue", parent, pzl, 1)
        if pzl in closedSet: continue
        closedSet[pzl] = parent
        for nbr in nodeToNodes[pzl]:
            if nbr in closedSet: continue
            if nbr == goal: return getPath(closedSet, pzl) + [nbr]
            newDist = dist + h(nbr, pzl)
            newF = h(nbr, goal) + newDist # f = h + g
            openSet.append((newF, nbr, pzl, newDist))
            addEdge("red", pzl, nbr, 1)
        openSet.sort()
        count+=1
    return []

def h(puzzle, goal):
    return calcDist(nodeToPos[puzzle][0], nodeToPos[puzzle][1], nodeToPos[goal][0], nodeToPos[goal][1])

def calcDist(y1,x1, y2,x2):
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions
    y1  = float(y1)
    x1  = float(x1)
    y2  = float(y2)
    x2  = float(x2)

    R   = 3958.76 # miles = 6371 km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    # approximate great circle distance with law of cosines
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def getPath(closedSet, goal): #Order Array
    order, key = [], goal
    while key:
        order.append(key)
        key = closedSet[key]
    order = order[::-1]
    return order

def printPath(path):
    parent = cityToNode[cityA] #Start ID
    sumDist = 0
    for node in path: #Node ID
        addEdge("green", parent, node, 2)
        edgeDist = h(parent, node)
        sumDist += edgeDist
        if node in nodeToCity:
            print("".join([nodeToCity[node], ": {}mi".format(round(edgeDist, 3))]))
        else: print("".join([node, ": {}mi".format(round(edgeDist, 3))]))
        parent = node
    print("Total Distance: {}mi".format(round(sumDist, 3)))

#Initialize Window
window = tkinter.Tk()
window.title("Railroads")
canvas = tkinter.Canvas(window, width = 1000, height = 500)
canvas.pack()
#Create Graph and Dictionaries
nodeToPos, nodeToNodes, nodeToCity, cityToNode = {}, {}, {}, {}
readNodes("rrNodes.txt", nodeToPos)
readEdges("rrEdges.txt", nodeToNodes)
readCities("rrNodeCity.txt", nodeToCity, cityToNode)
window.update()
#Find Shortest Path from 2 Cities
SPEED = 5 # Larger = Faster
cityA, cityB = determineCities(sys.argv[1:]) #Actual Names
idA, idB = cityToNode[cityA], cityToNode[cityB] #Identification Numbers
addPoint("yellow", idA)
addPoint("yellow", idB)
canvas.update
path = shortestPath(idA, idB)
printPath(path)
print("Number of Stations: {}".format(len(path)-1))
window.mainloop()