#matrix_builder.py
#builds ecludian distance matrixes

from __future__ import division
from custom import build_distance_matrix
import numpy
import pickle
import time
import sys

if __name__ == "__main__":
    try:
        size = int(sys.argv[1])
    except IndexError:
        print("no size given, defaulting to 10")
        size = 10
    t_start = time.time()
    distance_matrix = build_distance_matrix(size)
    with open("data/matrix"+str(size)+".p", "wb") as matrix_file:
        pickle.dump(distance_matrix, matrix_file)
    print("Matrix built\ntime taken "+str(round(time.time()-t_start,1))+"s")