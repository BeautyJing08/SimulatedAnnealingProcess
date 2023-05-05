import math
import random
import numpy as np


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
        if ((self.lx + self.ly) < 2): #這邊應該就不需要了，因為寫了一個合法lx ly限制的方法
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
    limit = 2 # x+y≥2
    randomlx = np.round(np.random.uniform(lx_dn, lx_up), 9)  # 創建一個落在lx範圍內的浮點數，取小數點後第九位
    randomly = np.round(np.random.uniform(ly_dn, ly_up), 9)
    if ((randomlx+randomly) < 2): #若創建出來的解是非法的，那就重新創造直到找到合法的組合
        legallxAndly()
    return randomlx,randomly


def SimulatedAnnealing(testPoint, temperature, FireReductionRadio):
    testPoint = testPoint
    temperature = temperature
    k = 1
    while temperature.temp > temperature.tempMin:
        print(f"現在是第{k}代，目前溫度是{temperature.temp}")
        # 創造一個新粒子
        randomlx, randomly = legallxAndly() #使用legallyAndly方法創造合法點
        tmpTestPoint = TestPoint(randomlx, randomly)
        if tmpTestPoint.fitness > testPoint.fitness:
            testPoint = tmpTestPoint
            temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
            print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
            print(f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio ({FireReductionRadio}) ** k ({k})")
        elif tmpTestPoint.fitness < testPoint.fitness:
            r = np.random.rand()  # 隨機創造0~1之間的數
            delta = tmpTestPoint.fitness - testPoint.fitness
            movePossibility = math.exp( delta / temperature.temp )
            print(f"delta={delta},temperature.temp={temperature.temp}")



            print(f"tmpP.F={tmpTestPoint.fitness},testP.F={testPoint.fitness}")
            print(f"因為新的粒子fitness < 初始粒子fitness")
            print(f"r= {r},movePossibility= {movePossibility} ,  delta= {delta}")
            if r < movePossibility: #若隨機變數r < 移動機率movePossibility
                testPoint = tmpTestPoint #就move粒子，讓新的取代舊的
                temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
                print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
                print(f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio ({FireReductionRadio}) ** k ({k})")
            else: #不移動粒子，但改變溫度
                temperature.temp = temperature.initialtemp * (FireReductionRadio ** k)
                print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")
                print(f"新溫度=> {temperature.temp} = temperature.initialtemp ({temperature.initialtemp}) * FireReductionRadio ({FireReductionRadio}) ** k ({k})")
        k += 1
        print()


# 建立lx,ly的限制 2≤x≤4 -1≤y≤2
lx_up = 4
lx_dn = 2
lx_lim = (lx_up - (lx_dn))

ly_up = 2
ly_dn = -1
ly_lim = (ly_up - (ly_dn))

# 創建初始粒子解
xAndyLim = 2  # x+y>2 (題目限制)
randomlx = np.round(np.random.uniform(lx_dn, lx_up), 9)  # 創建一個落在lx範圍內的浮點數，取小數點後第九位
randomly = np.round(np.random.uniform(ly_dn, ly_up), 9)
print(f"第一次創造的randomlx={randomlx}, randomly={randomly}")
n = 1
while (randomlx + randomly) < xAndyLim:
    randomlx = np.round(np.random.uniform(lx_dn, lx_up), 9)
    randomly = np.round(np.random.uniform(ly_dn, ly_up), 9)
    print(f"第{n}次創造的randomlx={randomlx}, randomly={randomly}")
    n += 1



def legalXandY(xAndyLim):
    randomlx = np.round(np.random.uniform(lx_dn, lx_up), 9)  # 創建一個落在lx範圍內的浮點數，取小數點後第九位
    randomly = np.round(np.random.uniform(ly_dn, ly_up), 9)





testPoint = TestPoint(randomlx, randomly)
print(f"初代資料： ")
print(f"lx={testPoint.lx},ly={testPoint.ly},fitness={testPoint.fitness}")

# 創建溫度

initialtemp = 1000
tempMin = 100
temperature = Temperature(initialtemp, tempMin)
print(f"temp={temperature.temp},tempMin={temperature.tempMin}")
print()

FireReductionRadio = 0.9

SimulatedAnnealing(testPoint, temperature, FireReductionRadio)

# a = math.exp(-112/500)
# print(a)