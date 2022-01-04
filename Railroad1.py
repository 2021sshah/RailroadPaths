# Siddharth Shah
import time, sys, tkinter
from math import pi, acos, sin, cos
from PIL import Image, ImageTk

def readNodes(fileName, nodeToPos):
    nodes = open(fileName, "r").read().splitlines()
    for node in nodes:
        space1 = node.index(" ")
        space2 = node.index(" ", space1+1)
        nodeToPos[node[:space1]] = (node[space1+1:space2], node[space2+1:])
    return nodeToPos

def readEdges(fileName, nodeToNodes):
    edges = open(fileName, "r").read().splitlines()
    for edge in edges:
        space = edge.index(" ")
        if edge[:space] not in nodeToNodes: nodeToNodes[edge[:space]] = []
        nodeToNodes[edge[:space]].append(edge[space+1:])
        if edge[space+1:] not in nodeToNodes: nodeToNodes[edge[space+1:]] = []
        nodeToNodes[edge[space+1:]].append(edge[:space])
    return nodeToNodes

def readCities(fileName, nodeToCity, cityToNode):
    cities = open(fileName, "r").read().splitlines()
    for city in cities:
        space = city.index(" ")
        nodeToCity[city[:space]] = city[space+1:]
        cityToNode[city[space+1:]] = city[:space]
    return (nodeToCity, cityToNode)

def determineCities(words):
    for i in range(1, len(words)):
        cities = (" ".join(words[:i]), " ".join(words[i:]))
        if cities[0] in cityToNode and cities[1] in cityToNode: return cities
    return("", "") #Cities Not Valid

def shortestPath(root, goal):
    if root == goal: return [root]
    openSet = [(h(root, goal), root, "", 0)]
    closedSet = {}
    while openSet:
        f, pzl, parent, dist = openSet.pop(0)
        if pzl in closedSet: continue
        closedSet[pzl] = parent
        for nbr in nodeToNodes[pzl]:
            if nbr in closedSet: continue
            if nbr == goal: return getPath(closedSet, pzl) + [nbr]
            newDist = dist + h(nbr, pzl)
            newF = h(nbr, goal) + newDist # f = h + g
            openSet.append((newF, nbr, pzl, newDist))
        openSet.sort()
    return []
    #return (("2383383", 5), ("1300287", 4), ("7343726", 3))

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
    parent = cityToNode[cityA]
    for ID in path:
        lst = []
        if ID in nodeToCity: lst.append(nodeToCity[ID])
        else: lst.append(ID)
        lst.append(str(h(parent, ID)))
        print("   ".join(lst))
        parent = ID

def createDisplay():
    window = tkinter.Tk()
    window.title("Railroads")
    canvas = tkinter.Canvas(window, width = 2000, height = 1500)
    canvas.pack()
    photo = tkinter.PhotoImage(file="rrMapCoarse.png")
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    window.mainloop()

startTime = time.time()
nodeToPos = readNodes("rrNodes.txt", {})
nodeToNodes = readEdges("rrEdges.txt", {})
nodeToCity, cityToNode = readCities("rrNodeCity.txt", {}, {})
cityA, cityB = determineCities(["Kansas", "City", "Las", "Vegas"]) #determineCities(sys.argv[1:])
path = shortestPath(cityToNode[cityA], cityToNode[cityB])
print(len(path))
printPath(path)
createDisplay() #Idk where this goes
print("Time Used: {}s".format(round(time.time() - startTime, 3)))