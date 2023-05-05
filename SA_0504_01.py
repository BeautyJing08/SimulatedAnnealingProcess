import math
import random

# 目標函數 f(x) = x^3 + 60x^2 + 900x + 100
def f(x):
    return x ** 3 + 60 * x ** 2 + 900 * x + 100

# 模擬退火演算法
def simulated_annealing(initial_state, temp, temp_min, alpha):
    current_state = initial_state
    best_state = current_state
    while temp > temp_min:
        # 在鄰域中隨機生成新的狀態
        new_state = random.randint(0, 31)
        # 計算目前狀態與新狀態之間的能量差
        delta_energy = f(new_state) - f(current_state)
        # 如果新狀態比目前狀態更好，直接接受新狀態
        if delta_energy > 0:
            current_state = new_state
            if f(current_state) > f(best_state):
                best_state = current_state
        # 否則以一定機率接受新狀態
        else:
            p = math.exp(delta_energy / temp)
            if random.random() < p:
                current_state = new_state
        # 降溫
        temp *= alpha
    return best_state

# 設定模擬退火演算法的初始參數
initial_state = random.randint(0, 31)
temp = 1000
temp_min = 1
alpha = 0.99

# 執行模擬退火演算法
best_state = simulated_annealing(initial_state, temp, temp_min, alpha)

# 輸出最佳解及其目標函數值
print("Best solution: x =", best_state)
print("Best objective function value:", f(best_state))

print("")
print()