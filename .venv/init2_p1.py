import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
import tqdm
from GA2_2 import evaluate,custom_mutate

# 定义停止条件：有三分之一满足条件则停止
def stop(top240):
    g=0
    for ind in top240:
        if ind.fitness.values[0]<10**10:
            g+=1
        if g>=80:
            return True
    return False

# 定义约束条件值
tc=0
sc=1
store_history=[2*2.82*10**4]
t=1

NGEN = 50
P_SIZE=500
def init(population, toolbox):
    gen=1
    pbar=tqdm.tqdm(total=NGEN,desc='init2_p1 running')
    while gen<=NGEN:
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.3)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        top240 = tools.selBest(population, k=240)
        if stop(top240):
            print("Good!Stop at generation:",gen)
            pbar.close()
            break
        else:
            if gen<=49:
                gen+=1
                pbar.update(1)
                continue 
            else:
                gen=1
                pbar.reset()
                continue
    return top240


def get_res(_):
    toolbox = base.Toolbox()
    # 注册个体和种群
    toolbox.register("attr_int", np.random.randint, 1, 9,size=50)
    toolbox.register("attr_bool", np.random.randint, 0, 2,size=50)
    toolbox.register("con_xy",lambda: np.hstack((toolbox.attr_int(), toolbox.attr_bool())).tolist())
    toolbox.register("individual", lambda:creator.Individual(toolbox.con_xy()))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate,t,store_history,tc,sc)
    # 注册遗传操作
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", custom_mutate, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=15)

    # 运行遗传算法
    population = toolbox.population(n=P_SIZE)
    return init(population, toolbox)
    
