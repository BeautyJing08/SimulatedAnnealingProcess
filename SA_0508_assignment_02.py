# chatGPT 告訴的計算程式距離方法

import math
import random
import numpy as np
import matplotlib.pyplot as plt

cities = ['A', 'B', 'C', 'D', 'E']
#
DMatrix = np.array([[0, 1, 2, 3, 4, 5],
                    [1, 0, 5, 8, 10, 12],
                    [2, 5, 0, 20, 10, 5],
                    [3, 8, 20, 0, 15, 2],
                    [4, 10, 10, 15, 0, 3],
                    [5, 12, 5, 2, 3, 0]])

# 計算 a-b-c-d-e-a 的總距離
path = ['A', 'B', 'C', 'D', 'E', 'A']
pathList= []
pathList.append(path)





def calculateDistance(path):
    total_distance = 0
    for i in range(len(path) - 1):
        this_city = path[i]
        next_city = path[i + 1]
        index_this = cities.index(this_city)
        index_next = cities.index(next_city)
        distance = DMatrix[index_this][index_next]
        total_distance += distance
    return  total_distance

# 顯示結果
print(f"{path} 的總距離為 {total_distance}")
