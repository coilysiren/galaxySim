#animate.py

from __future__ import division
import time
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def plotter ():
	plt.ion()
	npframes = numpy.load("output.npy")
	xs = range(npframes[0].shape[0]+1)
	ys = range(npframes[0].shape[1]+1)
	X,Y = numpy.meshgrid(xs,ys)
	img_list = plt.pcolormesh(X,Y,npframes[0],cmap="hot")
	for i in range(1,len(npframes)):
	    img_list.set_array(npframes[i].ravel())
	    img_list.autoscale()
	    plt.savefig("figure"+str(i)+".png")
	    plt.draw()
	    time.sleep(0.025)

def imager ():
	plt.ion()
	npframes = numpy.load("output.npy")
	xs = range(npframes[0].shape[0]+1)
	ys = range(npframes[0].shape[1]+1)
	X,Y = numpy.meshgrid(xs,ys)
	img_list = plt.pcolormesh(X,Y,npframes[0],cmap="hot")
	for i in range(1,len(npframes)):
	    img_list.set_array(npframes[i].ravel())
	    img_list.autoscale()
	    plt.savefig("figure"+str(i)+".png")

def giffer ():
	'''make gif'''
	#deps
	__author__ = 'Robert'
	from images2gif import writeGif
	from PIL import Image
	imager()
	#code
	file_names = sorted([fn for fn in os.listdir('.') if fn.endswith('.png')])
	print(file_names)
	images = [Image.open(fn) for fn in file_names]
	filename = "plot_gif.gif"
	writeGif(filename, images, duration=0.2)
	

if __name__ == "__main__":
	#plotter()
	#imager()
	giffer()
