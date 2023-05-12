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
    random.shuffle(solutionArray)
    return SolutionArray(solutionArray)  # 返回 SolutionArray 物件


def getNeighborSolution(solutionArray):  # 生成旁邊的解
    solutionArray = solutionArray
    pos1 = random.randint(0, len(solutionArray.array) - 1)
    pos2 = random.randint(0, len(solutionArray.array) - 1)
    if pos1 == pos2:
        getNeighborSolution(solutionArray)
    new_array = solutionArray.array.copy()  # 複製原始陣列
    new_array[pos1], new_array[pos2] = new_array[pos2], new_array[pos1]  # 交換位置
    new_fitness = fitnessFunction(WorkMatrix, new_array)  # 計算新的 fitness
    return SolutionArray(new_array)  # 返回新的 SolutionArray 物件


def SimulatedAnnealing(WorkMatrix, temperature):
    iterationNum = 0
    testArrayList = []
    gBestList = []  # 有更好的gBest時，就存進來
    gBestChangeIndexList = []  # 這是

    #### 初代解 ####
    testArray = getNewSolution()
    print(
        f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

    gBestArray = testArray  # 同時創造一個新的gBestArray來記錄
    # print(f"第{iterationNum}代，gBestarray= {gBestArray.array}, fitness= {gBestArray.fitness} ")
    testArrayList.append(testArray)
    while temperature.temp > temperature.tempMin:
        iterationNum += 1
        tmpTestArray = getNeighborSolution(testArray)
        ### 第一個情況，新的解比舊的解好 ###
        if tmpTestArray.fitness > testArray.fitness:
            # print(f"tmpTestArray.fitness={tmpTestArray.fitness} > testArray.fitness={testArray.fitness}")

            testArray = tmpTestArray

            if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
            print(
                f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")
            gBestList.append(gBestArray)
            ###############有加這句的話，就是沒有更好的也插進來##################

            if tmpTestArray.fitness > gBestArray.fitness:
                gBestArray = tmpTestArray
                gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好
                # print(f"第{iterationNum}代，gBestArray= {gBestArray.array}, gBestfitness= {gBestArray.fitness}")
                # gBestList.append(gBestArray)

        ### 第二個情況，新的解沒有比舊的解好 # 就要計算 delta & movePossibility & 隨機生成 r

        elif tmpTestArray.fitness < testArray.fitness:
            r = np.random.rand()  # 隨機創造0~1之間的數
            delta = tmpTestArray.fitness - testArray.fitness
            movePossibility = math.exp(delta / temperature.temp)
            # print(f"delta={delta},temperature.temp={temperature.temp}")
            #
            # print(f"因為新的粒子fitness < 初始粒子fitness")
            # print(f"tmpP.F={tmpTestArray.fitness},testP.F={testArray.fitness}")
            # print(f"r= {r:.2f},movePossibility= {movePossibility:.2f} ,  delta= {delta}")

            if r < movePossibility:  # 若隨機變數r < 移動機率movePossibility
                testArray = tmpTestArray  # 就move粒子，讓新的取代舊的
                if iterationNum % 3 == 0:
                    temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
                print(
                    f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

                ###############有加這句的話，就是沒有更好的也插進來##################
                # gBestList.append(gBestArray)
                if tmpTestArray.fitness > gBestArray.fitness:
                    gBestArray = tmpTestArray
                    gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好
                    # gBestList.append(gBestPoint)
        else:  # 不移動粒子，但改變溫度

            if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
            print(
                f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

            ###############有加這句的話，就是沒有更好的也插進來##################
            # gBestList.append(gBestArray)

        ####把這個iteration的解裝起來
        testArrayList.append(testArray)

    # iterationNum += 1
    print()
    return testArrayList, gBestList, gBestChangeIndexList, iterationNum


######## STEP 02 設定溫度  ####################################
# 創建溫度


print("M11105102")
print("Jing's SA_assignment")
initialtemp = 300
tempMin = 0.5
temperature = Temperature(initialtemp, tempMin)
print(f"temp={temperature.temp}\ttempMin={temperature.tempMin}")
print()

####### STEP 03 執行退火演算法 SimulatedAnnealing  #############

testArrayList, gBestList, gBestChangeIndexList, iterationNum = SimulatedAnnealing(WorkMatrix, temperature)

# for i in gBestList:
#     print(i.fitness)

## 創建 testArrayListFitness #把每一代的fitness裝進去
testArrayListFitness = []
for i in testArrayList:
    testArrayListFitness.append(i.fitness)
print(testArrayListFitness)
print(len(testArrayListFitness))
print(iterationNum + 1)

## 把 gBestChangeIndexList 丟到 testArrayListFitness找到轉折點
## 這是要拿來畫得到更好的gBest圖點圖

gBestChange_index_fitness = []
print(gBestChangeIndexList)
for i in gBestChangeIndexList:
    gBestChange_index_fitness.append(testArrayListFitness[i])

print(gBestChange_index_fitness)






################## STEP 04 繪圖 #############################
###版本一：每一個fitness跑的趨勢####

iteration_ = np.arange(0, len(testArrayListFitness), 1)
plt.xlabel("Generation")
plt.ylabel("Fitness,f Maximum")
plt.plot(iteration_, testArrayListFitness)  #
plt.title("Jing_SA")
plt.scatter(gBestChangeIndexList, gBestChange_index_fitness, alpha=0.3, c="r")
plt.show()
