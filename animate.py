#animate.py

import time
import numpy
import PIL
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import images2gif

def giffer ():
    plt.ion()
    npframes = numpy.load("output.npy")
    xs = range(npframes[0].shape[0]+1)
    ys = range(npframes[0].shape[1]+1)
    X,Y = numpy.meshgrid(xs,ys)
    dataList = plt.pcolormesh(X,Y,npframes[0],cmap="hot")
    images = list()
    for i in range(1,len(npframes)):
        thisFig = "figure"+str(i)+".jpg"
        dataList.set_array(npframes[i].ravel())
        dataList.autoscale()
        plt.savefig(thisFig)
        images.append(PIL.Image.open(thisFig))
        os.remove(thisFig)
    animName = "plot_gif.gif"
    images2gif.writeGif(filename=animName, images=images, duration=0.2, repeat=False)

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
        plt.draw()
        time.sleep(0.025)
    

if __name__ == "__main__":
    plotter()
    #giffer()