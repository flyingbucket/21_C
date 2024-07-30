import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
from Q2_2 import store, trans_con, store_con, cost
from tqdm import tqdm,trange

# 假设已经定义了目标函数 cost 和约束条件 trans_con, store_con
def check(individual):
    x = individual[:50]
    y = individual[50:]
    for i in x:
        if i==0:
            return False
    for i in y:
        if i>1:
            return False
    return True

def evaluate(t,store_history,individual):
    x = individual[:50]
    y = individual[50:]
    if trans_con(x, y, t) < 0 or store_con(x, y, t, store_history) < 0:
        return 10**10,  # 惩罚不满足约束条件的解
    elif not check(individual):
        return 10**10,  # 惩罚不满足约束条件的解
    else:
        return cost(x, y, t, store_history),

# 创建适应度最小化类型
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# 注册个体和种群
toolbox.register("attr_int", np.random.randint, 1, 9,size=50)
toolbox.register("attr_bool", np.random.randint, 0, 2,size=50)
toolbox.register("con_xy",lambda: np.hstack((toolbox.attr_int(), toolbox.attr_bool())).tolist())
toolbox.register("individual", lambda:creator.Individual(toolbox.con_xy()))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# so far,so good
# breakpoint()


# 注册遗传操作
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=8, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def GA(t, store_history):
    population = toolbox.population(n=10)

    # 注册评估函数
    toolbox.register("evaluate", evaluate,t,store_history)
    # 评估种群
    fitnesses = list(map(lambda ind: toolbox.evaluate(ind), population))
    
    for ind, fit in tqdm(zip(population, fitnesses),total=len(population), desc="Evaluating Population"):
        ind.fitness.values = fit
    # breakpoint()

    # 进化过程
    population,log= algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, verbose=True)

    # 找到当前周的最佳解
    best_individual = tools.selBest(population, k=1)[0]
    best_x = best_individual[:50]
    best_y = best_individual[50:]
    best_cost = best_individual.fitness.values[0]

    # 更新库存记录
    # if t == 1:
    #     current_store = store(best_x, best_y, t, [])
    # else:
    #     current_store = store(best_x, best_y, t, store_history)
    # store_history.append(current_store)
    current_store=store(best_x, best_y, t, store_history)
    store_history.append(current_store)
    return best_x, best_y, best_cost

if __name__ == '__main__':
    store_history = [2*2.82*10**4]
    res_x = []
    res_y = []
    res_cost = []
    # breakpoint()
    for t in trange(1, 25):
        best_x, best_y, best_cost = GA(t, store_history)
        res_x.append(best_x)
        res_y.append(best_y)
        res_cost.append(best_cost)

    res_x = pd.DataFrame(res_x)
    res_y = pd.DataFrame(res_y)
    res_cost = pd.DataFrame(res_cost)

    # 保存结果
    res_x.to_excel('GA_x.xlsx', index=False)
    res_y.to_excel('GA_y.xlsx', index=False)
    res_cost.to_excel('GA_cost.xlsx', index=False)
    
    print("Done!")
