import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
import tqdm
import random
import json
from GA2_2 import evaluate,custom_mutate
from init2_run_p1 import run_p1

# 定义初始种群
init_space=run_p1()
current_space=init_space

# 定义变异和交叉
toolbox = base.Toolbox()
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", custom_mutate, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=15)

# 定义全局变量
store_history=[2*2.82*10**4]
t=1
NGEN = 50

# 定义停止条件：有三分之一满足条件则停止
def stop(offspring):
    g=0
    for ind in offspring:
        if ind.fitness.values[0]<10**10:
            g+=1
        if g>=800:
            return True
    return False

def reg(i,current_space):
    '''注册第i轮筛选所用的约束条件值、评估函数和种群组件'''
    tc=1040*i
    sc=1+0.2*i
    toolbox.register("evaluate", evaluate,t,store_history,tc,sc)
    toolbox.register("individual", lambda:creator.Individual(random.choice(current_space)))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# 定义遗传算法
def GA_init(i,toolbox,current_space):
    reg(i,current_space)
    population = toolbox.population(n=2400)
    gen=0
    pbar = tqdm.tqdm(total=NGEN)
    while gen<=NGEN:
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=100)
        if stop(population):
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
    return population

# 开始收紧约束条件并筛选种群
for i in range(1,6):
    current_space=GA_init(i,toolbox,current_space)
search_space=current_space
with open(r'D:\mypython\math_modeling\21_C\data\search_space.txt', 'w') as file:
    json.dump(search_space, file)
