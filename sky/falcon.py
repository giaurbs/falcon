#!/usr/bin/env python3
from tabulate import tabulate
from matrix import build_matrix

#from matrix import sort_matrix
#matrix = sort_matrix(build_matrix()[1])
matrix = build_matrix()[1]

print(tabulate(matrix))
#print tabulate(matrix)
