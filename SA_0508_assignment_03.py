# 老師今年的作業跟之前不一樣啦囧

import math
import random
import numpy as np
import matplotlib.pyplot as plt


WorkMatrix = np.array([[67, 34, 32, 83, 38, 86, 85, 44, 25, 77],
                       [12, 74, 79, 51, 69, 42, 59, 17, 51, 22],
                       [32, 17, 87, 10, 70, 69, 67, 65, 28, 21],
                       [35, 13, 70, 37, 90, 59, 15, 84, 41, 40],
                       [73, 78, 74, 64, 34, 56, 18, 24, 56, 80],
                       [77, 39, 10, 34, 28, 53, 24, 36, 47, 81],
                       [76, 58, 51, 47, 36, 72, 33, 51, 78, 80],
                       [18, 83, 12, 19, 19, 78, 83, 44, 12, 15],
                       [90, 39, 56, 29, 25, 63, 29, 17, 48, 76],
                       [60, 39, 58, 40, 73, 33, 62, 30, 40, 59]])

####### STEP 01 __ 設定 method & class 來做後續使用 #############
## 創建
def fitnessFunction(WorkMatrix,solutionArray):
    fitness = 0 #初始化fitness
    print(f"solutionArray= {solutionArray}")
    solutionArray = [x - 1 for x in solutionA] #例如solutionarray=[3,1,2]-->轉換成[2,0,1]==>讓電腦可以讀取陣列

    print(f"solutionArray= {solutionArray}")
    for i in range(len(WorkMatrix)): #依序的跑每一行
        print(f"i={i}")
        fitness += WorkMatrix[i][solutionArray[i]] #fitness是WorkMatrix中的第i行，第幾個位置由solutionArray提供
        print(fitness)

    return  fitness #最後回傳fitness

## 創建溫度class
class Temperature():
    def __init__(self, initialtemp, tempMin):
        self.initialtemp = initialtemp
        self.temp = initialtemp
        self.tempMin = tempMin




