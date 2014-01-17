#custom.py

import sys
import math

def rotate (point_x, point_y, rads, center=(0,0)):
    newX = center[0] + (point_x-center[0])*math.cos(rads) - (point_y-center[1])*math.sin(rads)
    newY = center[1] + (point_x-center[0])*math.sin(rads) + (point_y-center[1])*math.cos(rads)
    return newX,newY

def sortkeys (data):
    out = list()
    for entry in data.keys(): out.append(entry)
    return sorted(out)

def proceed (text):
    go = input(text+" ")
    while not go == "yes":
        if go == "no":
            sure = input("WAIT WAIT ARE YOU SURE??? [yes/no] ")
            if sure == "yes": sys.exit()
        go = input(text+" [yes/no] ")

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