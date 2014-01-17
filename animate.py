#animate.py

import time
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

if __name__ == "__main__":
	plt.ion()
	npframes = numpy.load("output.npy")
	xs = range(npframes[0].shape[0]+1)
	ys = range(npframes[0].shape[1]+1)
	X,Y = numpy.meshgrid(xs,ys)
	img_list = plt.pcolormesh(X,Y,npframes[0],cmap="hot")
	for i in range(1,len(npframes)):
	    img_list.set_array(npframes[i].ravel())
	    img_list.autoscale()
	    plt.draw()
	    time.sleep(0.025)