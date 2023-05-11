# 紀錄每組gBest，並印出來

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

## 創建fitnessFunction Method
def fitnessFunction(WorkMatrix, solutionArray):
    fitness = 0  # 初始化fitness
    solutionArray = [x - 1 for x in solutionArray]  # 例如solutionarray=[3,1,2]-->轉換成[2,0,1]==>讓電腦可以讀取陣列
    for i in range(len(WorkMatrix)):  # 依序的跑每一行
        fitness += WorkMatrix[i][solutionArray[i]]  # fitness是WorkMatrix中的第i行，第幾個位置由solutionArray提供
    return fitness  # 最後回傳fitness


## 創建解class

class SolutionArray():
    def __init__(self, array):
        self.array = array
        self.fitness = fitnessFunction(WorkMatrix, array)  # 把這個array丟到找fitness的method計算出來


## 創建溫度class
class Temperature():
    def __init__(self, initialtemp, tempMin):
        self.initialtemp = initialtemp
        self.temp = initialtemp
        self.tempMin = tempMin


def SlowCooling(temperature, iterationNum):  # 降溫方法
    FireReductionRadio = 0.9  # 溫度下降的比例
    temperature.temp = temperature.initialtemp * (FireReductionRadio ** iterationNum)
    return temperature


def getNewSolution():
    solutionArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(solutionArray)  # 把solutionArray這個陣列重新排列
    return solutionArray

def getNeighborSolution(solutionArray): #生成旁邊的解
    pos1 = random.randint(0, len(solutionArray) - 1)
    pos2 = random.randint(0, len(solutionArray) - 1)
    solutionArray[pos1], solutionArray[pos2] = solutionArray[pos2], solutionArray[pos1]
    return solutionArray

def SimulatedAnnealing(testArray, gBestArray, temperature):
    gBestList = []
    gBestChangeIndexList = []
    print(f"第一輪進到退火演算法，溫度為 temperature.temp= {temperature.temp}")
    iterationNum = 1
    gBestList = []
    gBestChangeIndexList = []
    while temperature.temp > temperature.tempMin:
        tmpTestArray = SolutionArray(getNewSolution())
        ### 第一個情況，新的解比舊的解好 ###
        if tmpTestArray.fitness > testArray.fitness:
            testArray = tmpTestArray
            if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
            print(f"array= {testArray.array}, fitness= {testArray.fitness} ")
            print(f"temperature= {temperature.temp:.2f}")
            iterationNum += 1
            ###############有加這句的話，就是沒有更好的也插進來##################
            gBestList.append(gBestArray)
            if tmpTestArray.fitness > gBestArray.fitness:
                gBestArray = tmpTestArray
                gBestChangeIndexList.append(iterationNum) #紀錄哪一個iteration有變得更好
                # gBestList.append(gBestPoint)

        ### 第二個情況，新的解沒有比舊的解好 # 就要計算 delta & movePossibility & 隨機生成 r

        elif tmpTestArray.fitness < testArray.fitness:
            r = np.random.rand()  # 隨機創造0~1之間的數
            delta = tmpTestArray.fitness - testArray.fitness
            movePossibility = math.exp(delta / temperature.temp)
            print(f"delta={delta},temperature.temp={temperature.temp}")

            print(f"tmpP.F={tmpTestArray.fitness},testP.F={testArray.fitness}")
            print(f"因為新的粒子fitness < 初始粒子fitness")
            print(f"r= {r},movePossibility= {movePossibility} ,  delta= {delta}")

            if r < movePossibility:  # 若隨機變數r < 移動機率movePossibility
                testArray = tmpTestArray  # 就move粒子，讓新的取代舊的
                if iterationNum % 3 == 0:
                    temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
                print(f"array= {testArray.array}, fitness= {testArray.fitness} ")
                print(f"temperature= {temperature.temp:.2f}")
                ###############有加這句的話，就是沒有更好的也插進來##################
                gBestList.append(gBestArray)
                if tmpTestArray.fitness > gBestArray.fitness:
                    gBestArray = tmpTestArray
                    gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好
                    # gBestList.append(gBestPoint)

        else:  # 不移動粒子，但改變溫度

            if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
            print(f"array= {testArray.array}, fitness= {testArray.fitness} ")
            print(f"temperature= {temperature.temp:.2f}")
            ###############有加這句的話，就是沒有更好的也插進來##################
            gBestList.append(gBestPoint)
    iterationNum += 1
    print()

####### STEP 02 找到初代解  #############


# 創造初始解

print(f"初代解：")
testArray = SolutionArray(getNewSolution())
print(f"array= {testArray.array}, fitness= {testArray.fitness} ")

gBestArray = testArray  # 同時創造一個新的gBestArray來記錄
print(f"array= {gBestArray.array}, fitness= {gBestArray.fitness} ")

# 創建溫度

initialtemp = 300
tempMin = 100
temperature = Temperature(initialtemp, tempMin)
print(f"temp={temperature.temp},tempMin={temperature.tempMin}")
print()

SimulatedAnnealing(testArray, gBestArray, temperature)

