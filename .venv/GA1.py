import numpy as np
import pandas as pd
from tqdm import tqdm, trange
from Q2_2 import store, trans_con, store_con,cost
# Q2_2.py 已经定义了目标函数 cost 和约束条件 trans_con, store_con

def evaluate(individual, store_history, t):
    if len(individual) != 100:
        raise ValueError(f"individual 的长度应为 100,{len(individual)}")
    x = individual[:50]
    y = individual[50:]
    if trans_con(x, y, t) < 0 or store_con(x, y, t, store_history) < 0:
        return float('inf')  # 惩罚不满足约束条件的解
    return cost(x, y, t)

def init_population(pop_size, ind_size):
    return [np.random.randint(1, 9, size=ind_size).tolist() + np.random.randint(0, 2, size=ind_size).tolist() for _ in range(pop_size)]

def select(population, fitnesses, k=3):
    selected = []
    for _ in range(len(population)):
        aspirants = np.random.choice(len(population), k, replace=False)
        selected.append(population[min(aspirants, key=lambda i: fitnesses[i])])
    return selected

def crossover(parent1, parent2):
    point = np.random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return list(child1), list(child2)

def mutate(individual, indpb=0.2):
    for i in range(len(individual)):
        if np.random.rand() < indpb:
            if i < len(individual) // 2:
                individual[i] = np.random.randint(1, 9)
            else:
                individual[i] = np.random.randint(0, 2)
    return individual

def GA(t, store_history, pop_size=300, ind_size=50, cxpb=0.5, mutpb=0.2, ngen=120):
    population = init_population(pop_size, ind_size)
    fitnesses = [evaluate(ind, store_history, t) for ind in population]

    for gen in trange(ngen):
        offspring = select(population, fitnesses)
        # breakpoint()
        offspring1=[]
        # offspring = [crossover(offspring[i], offspring[i + 1]) for i in range(0, len(offspring), 2)]
        for i in range(0, len(offspring), 2):
            child1, child2 = crossover(offspring[i], offspring[i + 1])
            offspring.append(child1)
            offspring1.append(child1)
            offspring1.append(child2)
        offspring = [mutate(ind, mutpb) for ind in offspring1]
        population = offspring
        fitnesses = [evaluate(ind, store_history, t) for ind in population]

    best_individual = population[np.argmin(fitnesses)]
    best_x = best_individual[:50]
    best_y = best_individual[50:]
    best_cost = evaluate(best_individual, store_history, t)

    # 更新库存记录
    # if t == 1:
    #     current_store = store(best_x, best_y, t, [])
    # else:
    #     current_store = store(best_x, best_y, t, store_history)
    # store_history.append(current_store)

    # return best_x, best_y, best_cost
    current_store=store(best_x, best_y, t, store_history)
    store_history.append(current_store)
    return best_x, best_y, best_cost

if __name__ == '__main__':
    store_history = [2 * 2.82 * 10**4 ]
    res_x = []
    res_y = []
    res_cost = []
    for t in trange(1, 25):
        best_x, best_y, best_cost = GA(t, store_history)
        res_x.append(best_x)
        res_y.append(best_y)
        res_cost.append(best_cost)

    res_x = pd.DataFrame(res_x)
    res_y = pd.DataFrame(res_y)
    res_cost = pd.DataFrame(res_cost)

    # 保存结果
    res_x.to_excel('GA_x1.xlsx', index=False)
    res_y.to_excel('GA_y1.xlsx', index=False)
    res_cost.to_excel('GA_cost1.xlsx', index=False)
