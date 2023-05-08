# 這是要寫出assignment SA or TS 的第一次嘗試
# 要先寫出距離matrix 寫出城市間的距離

import math
import random
import numpy as np
import matplotlib.pyplot as plt

distanceMatrix = np.array([[0, 1, 2, 3, 4, 5],
                           [1, 0, 5, 8, 10, 12],
                           [2, 5, 0, 20, 10, 5],
                           [3, 8, 20, 0, 15, 2],
                           [4, 10, 10, 15, 0, 3],
                           [5, 12, 5, 2, 3, 0]])

Matrix = np.array([[0,4,3],
                   [4,0,6],
                   [3,6,0]])

print(distanceMatrix[3][2])
print(distanceMatrix.shape)
print(distanceMatrix.dtype)

# def fitnessFunction():
#

function01 = [0,2,5,4,1,0]
def calculateDistance(solutionarray):
    distance = 0
    for i in range(len(solutionarray)):
        distance += distanceMatrix[solutionarray[i]][solutionarray[(i+1) % len(solutionarray)]]
    distance += distanceMatrix[solutionarray[-1]][solutionarray[0]]
    return distance

distance01 = calculateDistance(function01)
print(distance01)

print("~~~~~~~~")