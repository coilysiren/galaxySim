#sim.py

import math
import time
import numpy
import matplotlib
import matplotlib.pyplot as plt
from custom import sortkeys
from custom import rotate
from custom import make_sphere

class emitters (object):
    def __init__ (self,x=0,y=0,v=0,m=0):
        self.x = x; self.y = y
        self.v = v; self.m = m 
    def emit(self,data):
        x = self.x; y = self.y
        v = self.v; m = self.m
        data[x,y] = add_mass(data[x,y],m,v,v)
        self.move()
        return data
    def move(self):
        self.x,self.y = rotate(self.x,self.y,math.pi/64)
        self.x = round(self.x)
        self.y = round(self.y)
        return 0

def fill (inp,size=100):
    for x in range(-size,size):
        for y in range(-size,size):
            inp[x,y] = dict(m=0,vx=0,vy=0)
    return inp

def diffuse (data,sphere,size):
    spreads = list()
    dataout = dict()
    dataout = fill(dataout,size)
    for x,y in data.keys():
        m = data[x,y]["m"]
        vx = data[x,y]["vx"]
        vy = data[x,y]["vy"]
        spreadinst = dict()
        if not m: pass
        elif m<1: spreadinst[x,y] = dict(vx=vx,vy=vy,m=m)
        else:
            #print("large mass")
            pil = dict()
            sumdist = 0
            for p,d in sphere.items():
                px,py = p[0]+x,p[1]+y
                try: 
                    sumdist += d
                    data[px,py]
                    pil[px,py] = d
                except KeyError: pass
            #print("pil ",pil)
            for p,d in pil.items():
                px,py = p[0],p[1]
                div = d/sumdist
                spreadinst[px,py] = dict(vx=vx,vy=vy,m=m*div)
            #print("spread ",spreadinst)
        spreads.append(spreadinst)
        del spreadinst
    for spreadinst in spreads:
        for p,val in spreadinst.items():
            x,y = p[0],p[1]
            m = val["m"]
            vx = val["vx"]
            vy = val["vy"]
            dataout[x,y] = add_mass(dataout[x,y],m,vx,vy)
    return dataout

def move (data,size,ejected_mass):
    dataout = dict()
    dataout = fill(dataout,size)
    for x,y in data.keys():
        m = data[x,y]["m"]
        if not m: continue
        vx = data[x,y]["vx"]
        vy = data[x,y]["vy"]
        xn = round(x+vx)
        yn = round(y+vy)
        try: dataout[xn,yn] = add_mass(dataout[xn,yn],m,vx,vy)
        except KeyError: ejected_mass += m; print("offmap")
    return dataout

def add_mass (data,m_n,vx_n,vy_n):
    m = data["m"]
    if not m:
        data["m"] = m_n
        data["vx"] = vx_n
        data["vy"] = vy_n
    else:
        vx = data["vx"]
        vy = data["vy"]
        data["m"] = m + m_n
        data["vx"] = (vx*m + vx_n*m_n)/data["m"]
        data["vy"] = (vy*m + vy_n*m_n)/data["m"]
    return data
    
def c_o_m (data):
    t_mass = 0
    w_pos = [0,0]
    for k,v in data.items():
        t_mass += v["m"]
        w_pos[0] += k[0]*v["m"]
        w_pos[1] += k[1]*v["m"]
    if t_mass:
        x = round(w_pos[0]/t_mass)
        y = round(w_pos[1]/t_mass)
        center = [x,y]
        return center,t_mass
    else: return [0,0],0
   
def gravitate (data,min_dist=9,sphere=0):
    fakeG = 0.02
    if sphere: 
        min_dist = 1
    center,t_mass = c_o_m(data)
    cx = center[0]
    cy = center[1]
    for x,y in data.keys():
        if not data[x,y]["m"]: continue
        if sphere:
            local_mass = dict()
            for px,py in sphere.keys():
                try:
                    pix = x+px; piy = y+py
                    lmass = data[pix,piy]["m"]
                    local_mass[pix,piy] = dict()
                    local_mass[pix,piy]["m"] = lmass
                except KeyError: pass
            center,t_mass = c_o_m(local_mass)
            cx = center[0]
            cy = center[1]
            if len(local_mass) == 1: continue
        dh = math.hypot(x-cx,y-cy)
        if dh<min_dist: continue
        acc = fakeG*t_mass/(dh**2)
        data[x,y]["vx"] += -(x-cx)*acc/(dh)
        data[x,y]["vy"] += -(y-cy)*acc/(dh)
    return data

def print_atts (data,tag,min_mass=0):
    mass = 0
    print("\n",tag,"\n")
    for k in sortkeys(data):
        v = data[k]
        if v["m"]>min_mass: print(k,v)
        mass += v["m"]
    print()
    center,mass = c_o_m(data)
    print("mass = ",round(mass))
    print("C.O.M = ",center,"\n")
    
def write_to_ndarray (data,size=0):
    npdata = numpy.zeros(shape=(size*2,size*2))
    for k,v in data.items():
        x = k[0] + abs(size)
        y = k[1] + abs(size)
        npdata[x,y] = v["m"]
    return npdata

def start ():
    ### [CONDITIONS] ###
    size = 100
    small = 10
    frames = 200
    em1 = emitters(x=size-small*3,y=0,v=0,m=10)
    em2 = emitters(x=-size+small*3,y=0,v=0,m=10)  
    ### [/CONDITIONS] ##  
    diff_sphere = make_sphere(math.ceil(small*2))
    grav_sphere = make_sphere(math.ceil(small*1.2))
    data = dict()
    data = fill(data,size)
    tstart = time.time()
    npframes = list()
    ejected_mass = 0
    for i in range(frames+1):
        print("step ",i)
        #print_atts(data,("step ",i),min_mass=1)
        data = em1.emit(data)
        data = em2.emit(data)
        data = gravitate(data,min_dist=small-1)#global
        data = gravitate(data,sphere=grav_sphere)#local
        data = move(data,size=size,ejected_mass=ejected_mass)
        data = diffuse(data,sphere=diff_sphere,size=size)
        npframes.append(write_to_ndarray(data,size))
    center,t_mass = c_o_m(data)
    info = list(["---Simulation Log File---\n",
                "Time taken: "+str(round(((time.time()-tstart)/60),1))+"minutes\n",
                "\n",
                "[Generation params]\n",
                "Size: "+str(2*size)+"x by "+str(2*size)+"y\n",
                "Frames: "+str(frames)+"\n",
                "\n",
                "[Results]\n",
                "Total mass: "+str(round(t_mass))+"\n", 
                "Center of mass: "+str(center[0])+"x "+str(center[1])+"y\n",
                ])
    with open("log.txt","w") as logfile:
        logfile.writelines(info)
    numpy.save("calculations",npframes)

start()