#custom.py

import math
import numpy

def rotate (point_x, point_y, rads, center=(0,0)):
    newX = center[0] + (point_x-center[0])*math.cos(rads) - (point_y-center[1])*math.sin(rads)
    newY = center[1] + (point_x-center[0])*math.sin(rads) + (point_y-center[1])*math.cos(rads)
    return newX,newY

def build_distance_matrix (size):
    distance_matrix = dict()
    known_distances = dict()
    for x1 in range(size):
        for y1 in range(size):
            distance_matrix[x1, y1] = numpy.empty((size, size))
            for (x2, y2), dont_need in numpy.ndenumerate(distance_matrix[x1, y1]):
                dx, dy = abs(x1-x2), abs(y1-x2)
                if (dx,dy) in known_distances.keys():
                    distance_matrix[x1, y1][x2, y2] = known_distances[dx,dy]
                else:
                    dist =  math.hypot(dx, dy)
                    known_distances[dx,dy] = dist
                    known_distances[dy,dx] = dist
                    distance_matrix[x1, y1][x2, y2] = dist
                distance_matrix[x1, y1][x2, y2] = math.hypot(dx, dy)
    return distance_matrix

def sortkeys (data):
    out = list()
    for entry in data.keys(): out.append(entry)
    return sorted(out)

def make_sphere (r): 
    inr = set()
    for x in range(r+1):
        for y in range(r+1):
            if math.hypot(x,y)<=r:
                inr.add((x,y))
                inr.add((-x,y))
                inr.add((x,-y))
                inr.add((-x,-y))
    dmap = dict()
    for x,y in inr:
        dmod = r+1-math.hypot(x,y)
        dmap[x,y] = dmod
    return dmap