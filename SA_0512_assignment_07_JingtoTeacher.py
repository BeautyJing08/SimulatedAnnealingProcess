###### M11105102 王菁 SA and TS assignment ##########
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import time

start = time.process_time()
########## STEP 00 __ 設定workMatrix ######################

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
def fitnessFunction(WorkMatrix, solutionArray):  ##用來計算Fitness
    fitness = 0  # 初始化fitness
    solutionArray = [x - 1 for x in solutionArray]  # 例如solutionarray=[3,1,2]-->轉換成[2,0,1]==>讓電腦可以讀取陣列
    for i in range(len(WorkMatrix)):  # 依序的跑每一行
        fitness += WorkMatrix[i][solutionArray[i]]  # fitness是WorkMatrix中的第i行，第幾個位置由solutionArray提供
    return fitness  # 最後回傳fitness


## 創建解class

class SolutionArray():  ##創建Solution時，同時計算fitness
    def __init__(self, array):
        self.array = array
        self.fitness = fitnessFunction(WorkMatrix, array)  # 把這個array丟到找fitness的method計算出來


## 創建溫度class
class Temperature():
    def __init__(self, initialtemp, tempMin): #創建溫度的時候，要丟入原始溫度 & 終止計算的最小溫度
        self.initialtemp = initialtemp
        self.temp = initialtemp #溫度會 == 初始溫度
        self.tempMin = tempMin


## 設定降溫method
def SlowCooling(temperature, iterationNum):  # 降溫方法
    FireReductionRadio = 0.9  # 溫度下降的比例
    temperature.temp = temperature.initialtemp * (FireReductionRadio ** iterationNum)
    return temperature


## 創建新solution方法
def getNewSolution(WorkMatrix):
    WorkMatrixRowNum = WorkMatrix.shape[0]  # 讀取WorkMatrix共有幾個row
    array = []
    for i in range(WorkMatrixRowNum):  # range(3) = [0,1,2]
        array.append(i)  # 這邊的solutionArray 會從0開始
    array = [x + 1 for x in array] #所以要讓 solutionArray 內的值都+1
    random.shuffle(array) #打亂 solutionArray 的內部順序
    return SolutionArray(array)  # 返回 SolutionArray 物件

## 創建 生成旁邊解 的 method
def getNeighborSolution(solutionArray):  # 生成旁邊的解
    solutionArray = solutionArray
    pos1 = random.randint(0, len(solutionArray.array) - 1)
    pos2 = random.randint(0, len(solutionArray.array) - 1)
    if pos1 == pos2: #若這麼碰巧的pos1 == pos2 ((會變成新的tmparray沒有更新))，所以重新執行這個method
        getNeighborSolution(solutionArray) # 重新執行
    new_array = solutionArray.array.copy()  # 複製原始陣列
    new_array[pos1], new_array[pos2] = new_array[pos2], new_array[pos1]  # 交換位置
    new_fitness = fitnessFunction(WorkMatrix, new_array)  # 計算新的 fitness
    return SolutionArray(new_array)  # 返回新的 SolutionArray 物件

## 創建 退火演算法的 method
def SimulatedAnnealing(WorkMatrix, temperature): #要把 workMatrix & 溫度丟進去
    iterationNum = 0 #從第0代開始
    testArrayList = []
    gBestList = []  # 有更好的gBest時，就存進來
    gBestChangeIndexList = []  # 這是索引gBest更動時的位置 ((後續可以丟到陣列中拿到fitness值

    #### 初代解 ####
    testArray = getNewSolution(WorkMatrix)
    print(f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

    gBestArray = testArray  # 同時創造一個新的gBestArray來記錄

    testArrayList.append(testArray)
    gBestList.append(gBestArray)
    #### 執行後續演算 ####
    while temperature.temp > temperature.tempMin: ##在溫度沒有低到"低溫標準"，都繼續執行計算
        iterationNum += 1
        tmpTestArray = getNeighborSolution(testArray) ##創建一個tmpTestArray ((從獲得鄰近解method創建
        ### 第一個情況，新的解比舊的解好 ###
        if tmpTestArray.fitness > testArray.fitness:
            testArray = tmpTestArray

            if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
            print( f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

            ### 若tmpTest > gBest 就要把索引值存到 gBestChangeIndexList

            if tmpTestArray.fitness > gBestArray.fitness:
                gBestArray = tmpTestArray
                gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好

        ### 第二個情況，新的解沒有比舊的解好 # 就要計算 delta & movePossibility & 隨機生成 r
        elif tmpTestArray.fitness < testArray.fitness:
            r = np.random.rand()  # 隨機創造0~1之間的數
            delta = tmpTestArray.fitness - testArray.fitness #參照公式
            movePossibility = math.exp(delta / temperature.temp) #參照公式

            ## 若 r < movePossibility
            if r < movePossibility:  # 若隨機變數r < 移動機率 movePossibility
                testArray = tmpTestArray  # 就move粒子，讓新的取代舊的
                if iterationNum % 3 == 0:
                    temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
                print(f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

                ### 若tmpTest > gBest 就要把索引值存到 gBestChangeIndexList

                if tmpTestArray.fitness > gBestArray.fitness:
                    gBestArray = tmpTestArray
                    gBestChangeIndexList.append(iterationNum)  # 紀錄哪一個iteration有變得更好
            else:
                if iterationNum % 3 == 0:
                    temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
                print(
                    f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

        else:  # 不移動粒子，但改變溫度

            if iterationNum % 3 == 0:
                temperature = SlowCooling(temperature, iterationNum)  # 每三個iteration就降溫一次
            print(f"第{iterationNum}代，array= {testArray.array}, fitness= {testArray.fitness}, temperature= {temperature.temp:.2f} ")

        #### 把這個iteration 的解裝起來
        testArrayList.append(testArray)
        gBestList.append(gBestArray)

    print()
    return testArrayList, gBestList, gBestChangeIndexList, iterationNum


######## STEP 02 設定溫度  ####################################
# 創建溫度

print("M11105102")
print("Jing's SA_assignment")
initialtemp = 3000
tempMin = 0
temperature = Temperature(initialtemp, tempMin) ### 創建溫度
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}") ### 印出 溫度設定
print()

####### STEP 03 執行退火演算法 SimulatedAnnealing  #####################

testArrayList, gBestList, gBestChangeIndexList, iterationNum = SimulatedAnnealing(WorkMatrix, temperature)

########################################################################

######## 創建 testArrayListFitness #把每一代的fitness裝進去
testArrayListFitness = []
for i in testArrayList:
    testArrayListFitness.append(i.fitness)
# print(testArrayListFitness)
# print(len(testArrayListFitness))
# print(iterationNum + 1)

######## 把 gBestChangeIndexList 丟到 testArrayListFitness找到轉折點
######## 這是要拿來畫得到更好的gBest圖點圖

gBestChange_index_fitness = []
# print(gBestChangeIndexList)
for i in gBestChangeIndexList:
    gBestChange_index_fitness.append(testArrayListFitness[i])

# print(gBestChange_index_fitness)

gBestListFitness = []
for i in gBestList:
    gBestListFitness.append(i.fitness)
# print(gBestListFitness)
print(f"初始溫度temp={temperature.initialtemp}\t低溫限制tempMin={temperature.tempMin}") ### 印出 溫度設定
print(f"總共執行了 {iterationNum} 代")
print(f"final_出現在第 {gBestChangeIndexList[-1]} 代, final_gBest = {gBestList[-1].array}, final_gBest_fitness= {gBestListFitness[-1]}")

end = time.process_time()

print(f"找到所有解的執行時間: ", (end - start))
################## STEP 04 繪圖 #############################

plt.title("Jing_SA")
iteration_ = np.arange(0, len(testArrayListFitness), 1)
plt.xlabel("Generation")
plt.ylabel("Fitness,f Maximum")
plt.plot(iteration_, testArrayListFitness, label="Test Array")  # 這是每一個iteration的fitness走勢

plt.plot(iteration_, gBestListFitness, c="black", alpha=0.3, label="gBest Array")  # 這是gBest的fitness走勢

# 這是把點位置的x軸==gBestChangeIndexList y軸==gBestChange_index_fitness 的文字描述((寫出座標位置))
for i in range(len(gBestChangeIndexList)):
    x = gBestChangeIndexList[i]
    y = gBestChange_index_fitness[i]
    plt.text(x, y + 3, f"({x}, {y})", fontsize=7, ha='center', va='bottom', alpha=0.5)

plt.scatter(gBestChangeIndexList, gBestChange_index_fitness, alpha=0.3, c="r" , label = "gBestChangePoint") #這是把gBestChange的點標示出來
plt.legend(loc='lower right')  # 顯示圖例 #放在圖的右下角

text = f'initialtemp={temperature.initialtemp}, tempMin={temperature.tempMin}'
plt.text(0.98, 0.2, text, fontsize=8, ha='right', va='bottom', transform=plt.gca().transAxes)
plt.show()
