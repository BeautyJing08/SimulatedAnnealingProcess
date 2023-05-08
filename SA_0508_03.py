#####這個version增加了「鄰近解的概念」，但是出來的答案並不好，而且有時候會失敗

import math
import random
import numpy as np
import matplotlib.pyplot as plt


## Problem 6
# Maximize 𝑓(𝑥,𝑦)=𝑠𝑖𝑛2(5𝜋(𝑥34−0.1))−(𝑦−1)4 2≤x≤4; -1≤y≤2; x+y≥2 Maximum =1 at (x,y)=(3.575,1)


def FitnessFunction(lx, ly):
    result = np.round(np.sin(5 * np.pi * ((pow(lx, 0.75) - 0.1)))
                      ** 2 - pow((ly - 1), 4), 9)
    return result


class TestPoint():
    def __init__(self, lx, ly):
        self.lx = lx
        self.ly = ly
        self.fitness = FitnessFunction(self.lx, self.ly)
        if ((self.lx + self.ly) < 2):  # 這邊應該就不需要了，因為寫了一個合法lx ly限制的方法
            self.fitness = -float('inf')


class Temperature():
    def __init__(self, initialtemp, tempMin):
        self.initialtemp = initialtemp
        self.temp = initialtemp
        self.tempMin = tempMin


# 創建時就會是合法的lx and ly method
def legallxAndly():
    ####首先設定lx ly的範圍
    lx_up = 4
    lx_dn = 2
    lx_lim = (lx_up - (lx_dn))
    ly_up = 2
    ly_dn = -1
    ly_lim = (ly_up - (ly_dn))
    ###################開始創造lx ly
    limit = 2  # x+y≥2
    randomlx = np.round(np.random.uniform(lx_dn, lx_up), 9)  # 創建一個落在lx範圍內的浮點數，取小數點後第九位
    randomly = np.round(np.random.uniform(ly_dn, ly_up), 9)
    if ((randomlx + randomly) < 2):  # 若創建出來的解是非法的，那就重新創造直到找到合法的組合
        legallxAndly()
    return randomlx, randomly


def NeighborlxAndly(lx, ly):
    ####首先設定lx ly的範圍
    lx_up = 4
    lx_dn = 2
    lx_lim = (lx_up - (lx_dn))
    ly_up = 2
    ly_dn = -1
    ly_lim = (ly_up - (ly_dn))
    ###################開始創造 Neighbor lx ly
    limit = 2  # x+y≥2
    initPercentage = 0.2  # 若在這個 randomPercen 之內，直接創造新的初始解
    r = np.random.rand()  # 隨機創造0~1之間的數
    if r < initPercentage:
        newLx, newLy = legallxAndly()
    delta_x = random.uniform(-1, 1)
    delta_y = random.uniform(-1, 1)
    # 首先是計算新的lx值
    newLx = lx + delta_x
    if newLx > lx_up:
        newLx = lx_up
    elif newLx < lx_dn:
        newLx = lx_dn
    # 輪到ly
    newLy = ly + delta_y
    if newLy > ly_up:
        newLy = ly_up
    elif newLy < ly_dn:
        newLy = ly_dn

    if ((newLx + newLy) < 2):  # 若創建出來的解是非法的，那就重新創造直到找到合法的組合
        newLx, newLy = legallxAndly()
    return newLx, newLy


def SimulatedAnnealing(testPoint, gBestPoint, temperature, FireReductionRadio):
    testPoint = testPoint
    temperature = temperature
    gBestPoint = gBestPoint
    k = 1  # 從第一代開始紀錄
    gBestList = []
    gBestChangeIndexList = []
    while temperature.temp > temperature.tempMin:
        print(f"現在是第{k}代，目前溫度是{temperature.temp}")
        # 創造一個新粒子
        # randomlx, randomly = legallxAndly()  # 使用legallyAndly方法創造合法點
        newlx, newly = NeighborlxAndly(testPoint.lx, testPoint.ly)
        tmpTestPoint = TestPoint(newlx, newly)
        if tmpTestPoint.fitness > testPoint.fitness:
            testPoint = tmpTestPoint
            temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
            print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
            print(
                f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio ({FireReductionRadio}) ** k ({k})")
            ###############有加這句的話，就是沒有更好的也插進來##################
            gBestList.append(gBestPoint)
            if tmpTestPoint.fitness > gBestPoint.fitness:
                gBestPoint = tmpTestPoint
                gBestChangeIndexList.append(k)
                # gBestList.append(gBestPoint)

        elif tmpTestPoint.fitness < testPoint.fitness:
            r = np.random.rand()  # 隨機創造0~1之間的數
            delta = tmpTestPoint.fitness - testPoint.fitness
            movePossibility = math.exp(delta / temperature.temp)
            print(f"delta={delta},temperature.temp={temperature.temp}")

            print(f"tmpP.F={tmpTestPoint.fitness},testP.F={testPoint.fitness}")
            print(f"因為新的粒子fitness < 初始粒子fitness")
            print(f"r= {r},movePossibility= {movePossibility} ,  delta= {delta}")
            if r < movePossibility:  # 若隨機變數r < 移動機率movePossibility
                testPoint = tmpTestPoint  # 就move粒子，讓新的取代舊的
                temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
                print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
                print(
                    f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio ({FireReductionRadio}) ** k ({k})")
                ###############有加這句的話，就是沒有更好的也插進來##################
                gBestList.append(gBestPoint)
                if tmpTestPoint.fitness > gBestPoint.fitness:
                    gBestPoint = tmpTestPoint
                    gBestChangeIndexList.append(k)
                    # gBestList.append(gBestPoint)

            else:  # 不移動粒子，但改變溫度
                temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
                print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
                print(
                    f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio ({FireReductionRadio}) ** k ({k})")
                ###############有加這句的話，就是沒有更好的也插進來##################
                gBestList.append(gBestPoint)
        k += 1
        print()

    return gBestList, k, gBestChangeIndexList


#######################上面定義完要用到的class and method後要來執行程式##########

# 創建初始粒子解

randomlx, randomly = legallxAndly()  # 使用legallyAndly方法創造合法點
testPoint = TestPoint(randomlx, randomly)
gBestPoint = TestPoint(randomlx, randomly)
gBestList = []
gBestChangeIndexList = []
print(f"初代資料： ")
print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
print(f"gBestlx= {gBestPoint.lx}, gBestly= {gBestPoint.ly}, gBest.F= {gBestPoint.fitness}")

# 創建溫度

initialtemp = 300
tempMin = 100
temperature = Temperature(initialtemp, tempMin)
print(f"temp={temperature.temp},tempMin={temperature.tempMin}")
print()

FireReductionRadio = 0.99  # 溫度下降的比例

##把gBestList, iterationNum gBestChangeIndexList 找出來
gBestList, iterationNum, gBestChangeIndexList = SimulatedAnnealing(testPoint, gBestPoint, temperature,
                                                                   FireReductionRadio)
# 建立一個gBest_history，把gBest的歷史紀錄全部記錄下來((即使沒有變得更好也記錄下來))
gBest_history = []

# print(f"gBest_history= {gBest_history}")
#######插入每一個gBest到gBest_history裡面
for i in gBestList:
    print(f"gBestlx= {i.lx}\t gBestly= {i.ly}\t gBestFitness= {i.fitness}")
    gBest_history.append(i.fitness)

# gBestChangeIndexListFitness ==> 找出這個變動值的位置之後，計算這個變動值的fitness((為了要放在圖表上清楚顯示))
gBestChangeIndexListFitness = []
for i in gBestChangeIndexList:
    gBestChangeIndexListFitness.append(gBest_history[i])

print(f"final_iterationNum= {iterationNum - 1}")  # 最後共有幾個迭代((這個數量代表溫度減少到沒有了))
print(f"gBestChangeIndexList= {gBestChangeIndexList}")

print(f"gBestChangeIndexListFitness ={gBestChangeIndexListFitness}")

############### 開始做圖 ######################

iteration_ = np.arange(0, iterationNum - 1, 1)
plt.xlabel("Generation")
plt.ylabel("Fitness,f Maximum")
plt.plot(iteration_, gBest_history)
plt.title("Jing_SA")
plt.scatter(gBestChangeIndexList, gBestChangeIndexListFitness, alpha=0.3, c="r")
plt.show()
