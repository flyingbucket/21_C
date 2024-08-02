import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
import random
from Q4 import store, trans_con, store_con, obj
from tqdm import tqdm,trange

# Q2_2.py 已经定义了目标函数 cost 和约束条件 trans_con, store_con
def check(individual):
    Q=individual[100]
    x = individual[:50]
    y = individual[50:100]
    for i in x:
        if i==0:
            return False
    for i in y:
        if i>1:
            return False
    return True

def check_p(population,p_size):
    che,a=0,p_size
    for ind in population:
        che+=ind.fitness.values[0]
    if che<a*10**10:
        return True
    
def evaluate(t,store_history,individual):
    x = individual[:50]
    y = individual[50:100]
    q=individual[-1]
    if trans_con(x, y, t) < 0 or store_con(x, y, t, q,store_history) < 0:
        return 10**10,  # 惩罚不满足约束条件的解
    elif not check(individual):
        return 10**10,  # 惩罚不满足约束条件的解
    else:
        return obj(x, y, t, q,store_history),

# 自定义变异函数
def custom_mutate(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            if i == 100:
                individual[i] = random.uniform(2.82, 5.64)  # Q的变异范围是2.82到5.64
            elif i < 50:
                individual[i] = random.randint(1, 8)  # 前50个元素的变异范围是1到8
            else:
                individual[i] = random.randint(0, 1)  # 后50个元素的变异范围是0、1
    return individual,

def con_xy():
    x = np.random.randint(1, 9, size=50)
    y = np.random.randint(0, 2, size=50)
    xy=np.hstack((x,y)).tolist()
    xy.append(random.uniform(2.82, 5.64))
    return xy

# 创建适应度最小化类型
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# 注册个体和种群
toolbox.register("attr_int", np.random.randint, 1, 9,size=50)
toolbox.register("attr_bool", np.random.randint, 0, 2,size=50)
toolbox.register("con_xy", con_xy)
toolbox.register("individual", lambda:creator.Individual(toolbox.con_xy()))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 注册遗传操作
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", custom_mutate,indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=15)

def GA(t, store_history):
    p_size=550
    population = toolbox.population(n=p_size)

    # 注册评估函数
    toolbox.register("evaluate", evaluate,t,store_history)
    # 评估种群
    fitnesses = list(map(lambda ind: toolbox.evaluate(ind), population))
    
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    #种群过差则重新生成种群
    m=0
    while not check_p(population,p_size):
        population = toolbox.population(n=p_size)
        fitnesses = list(map(lambda ind: toolbox.evaluate(ind), population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        m+=1
        if m>30:
            break
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    # 进化过程
    population,log= algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=30,stats=stats, verbose=True)

    # 找到当前周的最佳解
    best_individual = tools.selBest(population, k=1)[0]
    best_x = best_individual[:50]
    best_y = best_individual[50:100]
    best_Q = best_individual[100]
    best_cost = best_individual.fitness.values[0]

    # 更新库存记录
    current_store=store(best_x, best_y, t,best_Q,store_history)
    store_history.append(current_store)
    return best_x, best_y, best_cost,best_Q

if __name__ == '__main__':
    store_history = [2*2.82*10**4]
    res_x = []
    res_y = []
    res_fitness = []
    res_Q=[]
    t=1
    while t<=24:
        best_x, best_y, best_cost ,best_Q = GA(t, store_history)
        res_x.append(best_x)
        res_y.append(best_y)
        res_fitness.append(best_cost)
        res_Q.append(best_Q)
        if res_fitness[-1]<10**10:
            t+=1
        else:
            pass

    res_x = pd.DataFrame(res_x)
    res_y = pd.DataFrame(res_y)
    res_cost = pd.DataFrame(res_fitness)
    res_Q = pd.DataFrame(res_Q)
    store_history = pd.DataFrame(store_history)
    
    with pd.ExcelWriter(r'D:\mypython\math_modeling\21_C\result\Q4_result.xlsx') as writer:
        res_x.to_excel(writer, sheet_name='x', index=False)
        res_y.to_excel(writer, sheet_name='y', index=False)
        res_cost.to_excel(writer, sheet_name='fitness', index=False)
        res_Q.to_excel(writer, sheet_name='Q', index=False)
        store_history.to_excel(writer, sheet_name='store_history', index=False)
    print("Done!")
