import numpy as np
from deap import base, creator, tools, algorithms
from Q2_2 import store, trans_con, store_con,cost
# 假设已经定义了目标函数 cost 和约束条件 trans_con, store_con

def evaluate(individual):
    x = individual[:50]
    y = individual[50:]
    t = current_week  # 当前周数，需要在GA函数中定义
    if trans_con(x, y, t) < 0 or store_con(x, y, t) < 0:
        return float('inf'),  # 惩罚不满足约束条件的解
    return cost(x, y, t),

# 创建适应度最小化类型
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# 注册个体和种群
toolbox.register("attr_int", np.random.randint, 1, 9)
toolbox.register("attr_bool", np.random.randint, 0, 2)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_int, toolbox.attr_bool), n=50)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 注册评估函数
toolbox.register("evaluate", evaluate)

# 注册遗传操作
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=8, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def GA(t):
    population = toolbox.population(n=300)
    store_history = []

    for week in range(1, t + 1):
        global current_week
        current_week = week

        # 评估种群
        fitnesses = list(map(toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        # 进化过程
        population = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=240, verbose=False)

        # 找到当前周的最佳解
        best_individual = tools.selBest(population, k=1)[0]
        best_x = best_individual[:50]
        best_y = best_individual[50:]
        best_cost = best_individual.fitness.values[0]

        # 更新库存记录
        if week == 1:
            current_store = store(best_x, best_y, week, [])
        else:
            current_store = store(best_x, best_y, week, store_history)
        store_history.append(current_store)

    return best_x, best_y, best_cost

# 调用GA函数
best_x, best_y, best_cost = GA(24)
print("Best x:", best_x)
print("Best y:", best_y)
print("Best cost:", best_cost)
