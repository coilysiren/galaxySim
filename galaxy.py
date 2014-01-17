#galaxy.py

import numpy
import math
import matplotlib
import matplotlib.pyplot
import time
import pickle
from custom import rotate
from custom import build_distance_matrix

class galaxy (object):

    def __init__ (self, size, local_gravitation_threshold, emitter1, emitter2):
        MASS = 0; X = 1; Y = 2
        #parameters
        self.ejected_mass = 0
        self.size = size
        self.center_point = (int(size / 2), int(size / 2))
        self.local_gravitation_threshold = local_gravitation_threshold
        #emitters
        self.emitter1 = galaxy.emitter(self, emitter1[MASS], emitter1[X], emitter1[Y])
        self.emitter2 = galaxy.emitter(self, emitter2[MASS], emitter2[X], emitter2[Y])
        #data matrixes
        self.distance_matrix = pickle.load(open("matrix.p", "rb"))
        self.masses = numpy.zeros((size, size))
        self.x_velocities = numpy.zeros((size, size))
        self.y_velocities = numpy.zeros((size, size))
        self._masses = numpy.empty((size, size))
        self._x_velocities = numpy.empty((size, size))
        self._y_velocities = numpy.empty((size, size))

    def time_step (self):
        #zero out filler matrixes
        self._masses.fill(0)
        self._x_velocities.fill(0)
        self._y_velocities.fill(0)
        #emit
        self.emitter1.emit()
        self.emitter2.emit()
        #gravitate
        self._gravitate()
        #move
        self._move()
        #diffuse???
        #
        self.masses, self._masses = self._masses, self.masses
        self.x_velocities, self._x_velocities = self._x_velocities, self.x_velocities
        self.y_velocities, self._y_velocities = self._y_velocities, self.y_velocities

    def _add_to_location (self, mass, x, y, x_velocity, y_velocity):
        x = int(round(x)); y = int(round(y))
        #print("adding to point ",x,y)
        if x>self.size or x<0 or y>self.size or y<0:
            self.ejected_mass += mass
            print("offmap")
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
                x_velocity_change += relative_x*acceleration/distance_to
                y_velocity_change += relative_y*acceleration/distance_to
            self.x_velocities[location_here] += x_velocity_change
            self.y_velocities[location_here] += y_velocity_change
            #print("delta v ",x_velocity_change, y_velocity_change)                

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
    size = 100
    emitter1 = (10, round(size / 10), size / 2)
    emitter2 = (10, round(9 * size / 10), size / 2)
    galaxy = galaxy(size, 5, emitter1, emitter2)
    frames = list()
    frames.append(numpy.copy(galaxy.masses))
    for i in range(50):
        galaxy.time_step()
        frames.append(numpy.copy(galaxy.masses))
        print("Frame ",i)
    numpy.save("output", frames)