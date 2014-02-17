#matrix_builder.py

from __future__ import division
from custom import build_distance_matrix
import numpy
import pickle
import time
import sys

if __name__ == "__main__":
	try:
		size = sys.argv[1]
	except IndexError:
		print("no size give, defaulting to 10")
		size = 10
	t_start = time.time()
	distance_matrix = build_distance_matrix(size)
	with open("matrix.p", "wb") as matrix_file:
		pickle.dump(distance_matrix, matrix_file)
	print("time taken ",time.time()-t_start)