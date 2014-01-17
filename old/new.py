import numpy
import sympy
import matplotlib
import matplotlib.pyplot
import time

class galaxy (object):

    def __init__ (self, size, local_gravitation_threshold,
                  emitter1_mass, emitter1_x, emitter1_y,
                  emitter2_mass, emitter2_x, emitter2_y):
        self.size = size
        self.local_gravitation_threshold = local_gravitation_threshold
        self.masses = numpy.zeros((size, size))
        self.x_velocities = numpy.zeros((size, size))
        self.y_velocities = numpy.zeros((size, size))
        self.emitter1 = galaxy.emitter(self, emitter1_mass, emitter1_x, emitter1_y)
        self.emitter2 = galaxy.emitter(self, emitter2_mass, emitter2_x, emitter2_y)
        # center point
        self.center_point = sympy.Point(int(size / 2), int(size / 2))
        # bounce buffers
        self._masses = numpy.empty((size, size))
        self._x_velocities = numpy.empty((size, size))
        self._y_velocities = numpy.empty((size, size))

    def move (self):
        # clear "new" arrays
        self._masses.fill(0)
        self._x_velocities.fill(0)
        self._y_velocities.fill(0)
        # populate "new" arrays
        self.emitter1.emit()
        self.emitter2.emit()
        # swap "new" arrays in
        self.masses, self._masses = self._masses, self.masses
        self.x_velocities, self._x_velocities = self._x_velocities, self.x_velocities
        self.y_velocities, self._y_velocities = self._y_velocities, self.y_velocities

    def _add_to_location (self, mass, x, y, x_velocity, y_velocity):
        if not self._masses[x, y]:
            self._masses[x, y] = mass
            self._x_velocities[x, y] = x_velocity
            self._y_velocities[x, y] = y_velocity
        else:
            total_mass = self._masses[x, y] + mass
            self._masses[x, y] += total_mass
            self._x_velocities[x, y] = (self._x_velocities[x, y] * self._masses[x, y] + x_velocity * mass) / total_mass
            self._y_velocities[x, y] = (self._y_velocities[x, y] * self._masses[x, y] + y_velocity * mass) / total_mass

    class emitter (object):

        def __init__ (self, galaxy, mass, x, y):
            self.galaxy = galaxy
            self.mass = mass
            self.point = sympy.Point(x, y)
            self.x = x
            self.y = y

        def emit (self):
            self.galaxy._add_to_location(self.mass, self.x, self.y, 0, 0)
            self._move()

        def _move (self):
            self.point.rotate(sympy.pi / 64, self.galaxy.center_point)

if __name__ == "__main__":
    physics = (100, 5)
    emitter1 = (10, 50, 500)
    emitter2 = (10, 950, 500)
    galaxy = galaxy(physics, emitter1, emitter2)
    frames = list()
    frames.append(numpy.copy(galaxy.masses))
    for i in range(100):
        galaxy.move()
        frames.append(numpy.copy(galaxy.masses))
    numpy.save("output", frames)
    #images = matplotlib.pyplot.pcolormesh(frames[0], cmap = "hot")
    #for i in range(1, 100):
    #    images.set_array(frames[i].ravel())
    #    images.autoscale()
    #    matplotlib.pyplot.draw()
    #    time.sleep(0.05)
