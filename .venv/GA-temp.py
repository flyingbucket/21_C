import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
from functools import partial
from tqdm import tqdm, trange
from Q2_2 import store, trans_con, store_con,cost

def evaluate(individual, store_history, t):
    if len(individual) != 100:
        raise ValueError(f"individual 的长度应为 100,{len(individual)}")
    x = individual[:50]
    y = individual[50:]
    if trans_con(x, y, t) < 0 or store_con(x, y, t, store_history) < 0:
        return float('inf')  # 惩罚不满足约束条件的解
    return cost(x, y, t)

# 设置遗传算法参数
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 0, 2)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", partial(evaluate, store_history=store, t=t))
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# 运行遗传算法
population = toolbox.population(n=500)
NGEN = 1200
for gen in trange(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
top24 = tools.selBest(population, k=24)

