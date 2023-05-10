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

## 創建fitnessFunction Metod
def fitnessFunction(WorkMatrix, solutionArray):
    fitness = 0  # 初始化fitness
    solutionArray = [x - 1 for x in solutionArray]  # 例如solutionarray=[3,1,2]-->轉換成[2,0,1]==>讓電腦可以讀取陣列
    for i in range(len(WorkMatrix)):  # 依序的跑每一行
        fitness += WorkMatrix[i][solutionArray[i]]  # fitness是WorkMatrix中的第i行，第幾個位置由solutionArray提供
    return fitness  # 最後回傳fitness

## 創建解class

class SolutionArray():
    def __init__(self,array):
        self.array = array
        self.fitness = fitnessFunction(WorkMatrix,array) #把這個array丟到找fitness的method計算出來




## 創建溫度class
class Temperature():
    def __init__(self, initialtemp, tempMin):
        self.initialtemp = initialtemp
        self.temp = initialtemp
        self.tempMin = tempMin

def SlowCooling(temperature,iterationNum): #降溫方法
    FireReductionRadio = 0.9 #溫度下降的比例
    temperature.temp = temperature.initialtemp * (FireReductionRadio ** iterationNum)
    return temperature

def getNewSolution():
    solutionArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(solutionArray)  # 把solutionArray這個陣列重新排列
    return solutionArray


def SimulatedAnnealing(testArray, gBestArray, temperature):
    gBestList = []
    gBestChangeIndexList = []
    print(f"第一輪進到退火演算法，溫度為 temperature.temp= {temperature.temp}")
    iterationNum = 1
    while temperature.temp > temperature.tempMin:
        tmpTestArray = SolutionArray(getNewSolution())

        if tmpTestArray.fitness > testArray.fitness:
            testArray = tmpTestArray
            # temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
            temperature = SlowCooling(temperature, iterationNum) #降溫
            print(f"array= {testArray.array}, fitness= {testArray.fitness} ")
            print(f"temperature= {temperature.temp:.2f}")
            # print(f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio (0.99) ** k ({iterationNum})")
            iterationNum += 1


####### STEP 02 找到初代解  #############


# 創造初始解

print(f"初代解：")
testArray = SolutionArray(getNewSolution())
print(f"array= {testArray.array}, fitness= {testArray.fitness} ")

gBestArray = testArray #同時創造一個新的gBestArray來記錄
print(f"array= {gBestArray.array}, fitness= {gBestArray.fitness} ")



# 創建溫度

initialtemp = 300
tempMin = 100
temperature = Temperature(initialtemp, tempMin)
print(f"temp={temperature.temp},tempMin={temperature.tempMin}")
print()

SimulatedAnnealing(testArray, gBestArray, temperature)