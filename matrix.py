#!/usr/bin/env python

import sys
import os

vector = [2, 3, 6, 5]

matrix = [[1,3,9,2], [2,4,6,8]]

matrix1 = [[8,9,4,0],
          [1,4,4,7],
          [7,8,8,2],
          [0,6,0,1]]
matrix2 = [[2,5,2,6],
          [4,4,6,3],
          [4,5,5,1],
          [2,4,6,8]]

def vector_multiply(vector, val):
    return [x*val for x in vector]

def matrix_transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def vector_matrix_multiplication(vector, matrix):
    if len(vector) != len(matrix):
        raise Exception("Undefined calculation")

    # Create a result vector
    result = [0] * len(matrix[0])

    for col in range(len(matrix[0])):
        for element in range(len(matrix)):
            result[col] += matrix[element][col] * vector[element]

    return result

def matrix_matrix_multiplication(m1, m2):
    # Create result vector
    result = [None] * len(m1)

    # For every row in m1, multiply as a vector against m2
    for vector_idx in range(len(m1)):
        result[vector_idx] = vector_matrix_multiplication(m1[vector_idx], m2)

    return result

def identity_matrix(n):
    return [[1 if i==j else 0 for i in range(n)] for j in range(n)]

fh = open("output/hw_mult.csv", "w")
print >> fh, "matrix1 x matrix2"
print >> fh, matrix_matrix_multiplication(matrix1, matrix2)
fh.close()

fh = open("output/hw_inv_mult.csv", "w")
print >> fh, "identity_matrix(10):"
print >> fh, identity_matrix(10)
fh.close()

