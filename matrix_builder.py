#matrix_builder.py

from custom import build_distance_matrix
import numpy
import pickle
import time

if __name__ == "__main__":
	size = 25
	t_start = time.time()
	distance_matrix = build_distance_matrix(size)
	with open("matrix.p", "wb") as matrix_file:
		pickle.dump(distance_matrix, matrix_file)
	print("time taken ",time.time()-t_start)