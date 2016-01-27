#!/usr/bin/env python3

from matrix import build_matrix
from matrix import sort_matrix

matrix = sort_matrix(build_matrix()[1])

print(matrix[:20])
