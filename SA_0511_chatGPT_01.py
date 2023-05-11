import random
import math
import numpy as np
def calculate_fitness(solution, assignment):
    fitness = sum(assignment[i][j-1] for i, j in enumerate(solution))
    return fitness

def generate_random_solution(num_jobs):
    solution = list(range(1, num_jobs + 1))
    random.shuffle(solution)
    return solution

def generate_neighbour_solution(solution):
    # Perform a swap between two random positions in the solution
    pos1 = random.randint(0, len(solution) - 1)
    pos2 = random.randint(0, len(solution) - 1)
    solution[pos1], solution[pos2] = solution[pos2], solution[pos1]
    return solution

def acceptance_probability(current_fitness, new_fitness, temperature):
    if new_fitness > current_fitness:
        return 1.0
    else:
        return math.exp((new_fitness - current_fitness) / temperature)

def simulated_annealing(assignment, initial_temperature, cooling_rate, num_iterations):
    num_jobs = len(assignment)
    current_solution = generate_random_solution(num_jobs)
    current_fitness = calculate_fitness(current_solution, assignment)
    print(f"current_solution= {current_solution}, current_fitness= {current_fitness}")
    best_solution = current_solution.copy()
    best_fitness = current_fitness
    print(f"best_solution= {best_solution}, best_fitness= {best_fitness}")
    temperature = initial_temperature
    for i in range(num_iterations):
        new_solution = generate_neighbour_solution(current_solution)
        new_fitness = calculate_fitness(new_solution, assignment)

        probability = acceptance_probability(current_fitness, new_fitness, temperature)
        if random.random() < probability:
            current_solution = new_solution
            current_fitness = new_fitness

        if new_fitness > best_fitness:
            best_solution = new_solution
            best_fitness = new_fitness
        # print(f"current_solution= {current_solution}, current_fitness= {current_fitness}")
        print(f"best_solution= {best_solution}, best_fitness= {best_fitness}")
        temperature *= cooling_rate

    return best_solution, best_fitness

# 執行退火演算法
# assignment = [[12, 22, 58],
#               [39, 62, 65],
#               [20, 53, 15]]



assignment = np.array([[67, 34, 32, 83, 38, 86, 85, 44, 25, 77],
                       [12, 74, 79, 51, 69, 42, 59, 17, 51, 22],
                       [32, 17, 87, 10, 70, 69, 67, 65, 28, 21],
                       [35, 13, 70, 37, 90, 59, 15, 84, 41, 40],
                       [73, 78, 74, 64, 34, 56, 18, 24, 56, 80],
                       [77, 39, 10, 34, 28, 53, 24, 36, 47, 81],
                       [76, 58, 51, 47, 36, 72, 33, 51, 78, 80],
                       [18, 83, 12, 19, 19, 78, 83, 44, 12, 15],
                       [90, 39, 56, 29, 25, 63, 29, 17, 48, 76],
                       [60, 39, 58, 40, 73, 33, 62, 30, 40, 59]])

initial_temperature = 100.0
cooling_rate = 0.95
num_iterations = 1000

best_solution, best_fitness = simulated_annealing(assignment, initial_temperature, cooling_rate, num_iterations)

print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)

# num_jobs = 5
# solution = list(range(1, num_jobs + 1))
# print(solution)


a_solution =  [10, 5, 7, 3, 2, 4, 9, 6, 1, 8]
a_fitness = calculate_fitness(a_solution, assignment)
print(f"a_solution= {a_solution}, a_fitness= {a_fitness}")