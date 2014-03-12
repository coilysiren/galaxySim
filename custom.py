#custom.py

from __future__ import division
import math
import numpy

class partitionData (object):
    '''
    Partitions data into 2d or 3d boxes.

    [Input]
    data
        type: numpy ndarray
        a collection of the data to be partitioned

    [API]
    self.partitionToPoints[partition]
        type: dictionary
        all the points this partition holds
    self.pointToPartition[point]
        type: dictionary
        the partition this point is held in
    self.maxPartition
        type: int
        the number of the last partition
    self.partitionAverage[partition]
        type: dictionary
        stores the average for each partition
    self.calculateAvereage()
        stores the average of each partition's data into self.partitionAverage
    '''
    def __init__ (self, data):
        self.data = data
        self.partitionToPoints = dict()
        self.pointToPartition = dict()
        #check input
        assert type(data) is numpy.ndarray, "incorrect data type"
        try:
            sizeX, sizeY, sizeZ = data.shape
            boxSize = math.floor(((sizeX+sizeY+sizeZ)/3)**0.5)
            for (x, y, z), v in numpy.ndenumerate(data):
                boxX = x//boxSize
                boxY = y//boxSize
                boxZ = z//boxSize
                box = boxX+boxSize*boxY+(boxSize**2)*boxZ
                self.pointToPartition[(x,y,z)] = box
                try:
                    self.partitionToPoints[box].append((x,y,z))
                except KeyError:
                    self.partitionToPoints[box] = list()
                    self.partitionToPoints[box].append((x,y,z))
        except ValueError:
            sizeX, sizeY = data.shape
            boxSize = math.floor(((sizeX+sizeY)/2)**0.5)
            for (x, y), v in numpy.ndenumerate(data):
                boxX = x//boxSize
                boxY = y//boxSize
                box = boxX+boxSize*boxY
                self.pointToPartition[(x,y)] = box
                try:
                    self.partitionToPoints[box].append((x,y))
                except KeyError:
                    self.partitionToPoints[box] = list()
                    self.partitionToPoints[box].append((x,y))
        inBox = 0
        for k, v in self.partitionToPoints.items(): 
            inBox += len(v)
        #checks for some sort of obscure error
        assert inBox == data.size, "all data not placed in boxes"
        self.maxPartition = len(self.partitionToPoints)-1
        print(str(len(self.pointToPartition))+" data points -> "+str(len(self.partitionToPoints))+" partitions")

    def calculateAvereage (self, param=0):
        '''
        given a data set where data[i] = value, averages that value

        but if given a param, calculates the average of data[i][param]
        '''
        self.partitionAverage = dict()
        for partition, points in self.partitionToPoints.items():
            valueSum = 0
            numPoints = len(points)
            for point in points:
                if not param:
                    valueSum += self.data[point]
                else:
                    valueSum += self.data[point][param]
            self.partitionAverage[partition] = valueSum/numPoints


def rotate (point_x, point_y, rads, center=(0,0)):
    newX = center[0] + (point_x-center[0])*math.cos(rads) - (point_y-center[1])*math.sin(rads)
    newY = center[1] + (point_x-center[0])*math.sin(rads) + (point_y-center[1])*math.cos(rads)
    return newX,newY

def build_distance_matrix (size):
    dmBar = createProgressBar(size)
    dmBar.start
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
    
    dmBar.finish
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