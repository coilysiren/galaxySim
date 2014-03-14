#galaxy.py

from __future__ import division
import numpy
import math
import matplotlib
import matplotlib.pyplot
import time
import pickle
import sys
from custom import loopProgress
from custom import rotate
from custom import build_distance_matrix

class galaxy (object):

    def __init__ (self, size, emitterList):
        MASS = 0; X = 1; Y = 2
        #parameters
        self.ejected_mass = 0
        self.size = size
        self.center_point = (int(size / 2), int(size / 2))
        #emitters
        self.emitterList = emitterList
        for i, emitter in enumerate(self.emitterList):
            self.emitterList[i] = galaxy.emitter(self, emitter[MASS], emitter[X], emitter[Y])
        #data matrixes
        self.distance_matrix = pickle.load(open("data/matrix"+str(size)+".p", "rb")) #not tested yet!!!
        self.masses = numpy.zeros((size, size))
        self.x_velocities = numpy.zeros((size, size))
        self.y_velocities = numpy.zeros((size, size))
        self._masses = numpy.empty((size, size))
        self._x_velocities = numpy.empty((size, size))
        self._y_velocities = numpy.empty((size, size))

    def time_step (self):
        self._masses.fill(0)
        self._x_velocities.fill(0)
        self._y_velocities.fill(0)
        for emitter in self.emitterList:
            emitter.emit()
        self._gravitate()
        self._move()
        self._diffuse()
        self.masses, self._masses = self._masses, self.masses
        self.x_velocities, self._x_velocities = self._x_velocities, self.x_velocities
        self.y_velocities, self._y_velocities = self._y_velocities, self.y_velocities

    def _add_to_location (self, mass, x, y, x_velocity, y_velocity):
        try:
            x = int(round(x)); y = int(round(y))
        except ValueError:
            pass
        #print("adding to point ",x,y)
        if x>=self.size or x<0 or y>=self.size or y<0 or math.isnan(x) or math.isnan(y):
            self.ejected_mass += mass
            #print("offmap")
        elif self._masses[x, y] == 0:
            self._masses[x, y] = mass
            self._x_velocities[x, y] = x_velocity
            self._y_velocities[x, y] = y_velocity
        else:
            total_mass = self._masses[x, y] + mass
            self._masses[x, y] += total_mass
            self._x_velocities[x, y] = (self._x_velocities[x, y] * self._masses[x, y] + x_velocity * mass) / total_mass
            self._y_velocities[x, y] = (self._y_velocities[x, y] * self._masses[x, y] + y_velocity * mass) / total_mass

    def _move (self):
        for location, mass_here in numpy.ndenumerate(self.masses):
            X = 0; Y = 1
            if not mass_here: continue
            x_velocity = self.x_velocities[location]
            y_velocity = self.y_velocities[location]
            self._add_to_location(mass_here, location[X]+x_velocity, location[Y]+y_velocity, x_velocity, y_velocity)

    def _gravitate (self):
        for location_here, mass_here in numpy.ndenumerate(self.masses):
            X = 0; Y = 1; G = .1
            if not mass_here: continue
            distance_matrix_here = self.distance_matrix[location_here]
            acceleration_matrix = G * self.masses / (0.01+distance_matrix_here**2)
            x_velocity_change = 0
            y_velocity_change = 0
            for location_there, acceleration in numpy.ndenumerate(acceleration_matrix):
                if acceleration == 0 or (location_here == location_there): continue
                relative_x = location_there[X]-location_here[X]
                relative_y = location_there[Y]-location_here[Y]
                distance_to = distance_matrix_here[location_there[X], location_there[Y]]
                if distance_to == 0: continue
                x_velocity_change += relative_x*acceleration/distance_to
                y_velocity_change += relative_y*acceleration/distance_to
            self.x_velocities[location_here] += x_velocity_change
            self.y_velocities[location_here] += y_velocity_change
    #very experimental diffusion code
    '''
    def _diffuse (self):
        MASS = 0; X = 1; Y = 2
        spreads = list()
        for location, mass in numpy.ndenumerate(self.masses):
            if (not mass) or (mass<1): continue
            xVelocity = self.x_velocities[location]
            yVelocity = self.y_velocities[location]
            spreadinst = dict()
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
        for spreadinst in spreads:
            for point,value in spreadinst.items():
                x,y = point[0],point[1]
                m = value["m"]
                vx = value["vx"]
                vy = value["vy"]
                self._add_to_location(self.mass, self.x, self.y, 0, 0)
    '''
    class emitter (object):

        def __init__ (self, galaxy, mass, x, y):
            self.galaxy = galaxy
            self.mass = mass
            self.x = x
            self.y = y

        def emit (self):
            self.galaxy._add_to_location(self.mass, self.x, self.y, 0, 0)
            self._spin()

        def _spin (self):
            self.x, self.y = rotate(self.x, self.y, math.pi/128, self.galaxy.center_point)

if __name__ == "__main__":
    #argument parsing
    try: size = int(sys.argv[1])
    except IndexError:
        print("no size given, defaulting to 10")
        size = 10
    try: maxFrames = int(sys.argv[2])
    except IndexError:
        print("no frames given, defaulting to 20")
        maxFrames = 20
    #galaxy inits
    emitterTop = (10, round(size/10), size/2)
    emitterBottom = (10, round(9*size/10), size/2)
    emitterLeft = (10, size/2, round(size/10))
    emitterRight = (10, size/2, round(9*size/10))
    emitterCenter = (10, size/2, size/2)
    galaxy = galaxy(size, [emitterCenter])
    #loop inits
    frames = list()
    frames.append(numpy.copy(galaxy.masses))
    pb = loopProgress(maxFrames)
    for i in range(maxFrames):
        galaxy.time_step()
        frames.append(numpy.copy(galaxy.masses))
        pb.update(i)
    #save
    print("\nCreating: data/output_s"+str(size)+"_f"+str(maxFrames))
    numpy.save("data/output_s"+str(size)+"_f"+str(maxFrames), frames)