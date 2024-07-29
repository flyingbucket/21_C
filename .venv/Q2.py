import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
import tqdm

# 读取数据
suppliers_scores = pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\scores.xlsx', header=0)
headers = suppliers_scores.columns.tolist()
supplier_id_header = headers[1]
supplier_score_header = headers[2]
supplier_ids = suppliers_scores[supplier_id_header].values
supplier_scores = suppliers_scores[supplier_score_header].values
supplier=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\supply_expectation.xlsx', header=0)
resource_type=supplier['材料分类'].tolist()
rate_dict=dict(A=1/0.6,B=1/0.66,C=1/0.72)

# 计算各类材料生产率
con_rate=[]
for type in resource_type:
    rate=rate_dict[type]
    con_rate.append(rate)
con_rate=np.round(con_rate,2)
def x_ij(i,j):
    '''计算第i个供应商第j周的供应量'''
    return supplier.iloc[i,j+1]

# 定义决策变量
num_suppliers = 50

def obj1(y):
    '''目标函数1：最小化每周所需的供货商总数量'''
    return np.sum(y)


def obj2(y):
    '''目标函数2：最大化每周所获得的总分数'''
    total_score = np.sum(np.multiply(y, supplier_scores))
    num_selected_suppliers = np.sum(y)
    res=num_selected_suppliers/(total_score+0.001)   
    return res 


def cf(y):
    '''组合目标函数,权重各为50%,越小越好'''
    obj_1 = obj1(y)
    obj_2 = obj2(y)
    return 0.5 * obj_1 + 0.5 * obj_2 

# 定义约束条件
def constraint(y,t):
    x_ls=[x_ij(i,t) for i in range(num_suppliers)]
    x=np.array(x_ls)
    res=np.sum(np.multiply(np.multiply(x,y),con_rate))
    return res-2.82*10**4
# 定义适应度函数
def evaluate(individual):
    y = np.array(individual, dtype=int)
    t = 1  # 假设第1周
    obj_value = cf(y)
    constraint_value = constraint(y, t)
    if constraint_value < 0:
        return (float('inf'),)  # 惩罚违反约束的个体
    return (obj_value,)

# 设置遗传算法参数
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 0, 2)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=num_suppliers)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# 运行遗传算法
population = toolbox.population(n=500)
NGEN = 1200
for gen in tqdm.trange(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
top24 = tools.selBest(population, k=24)

# 输出结果
# print("Top 24 individuals:")
least=[]
for ind in top24:
    least.append(sum(ind))
print(max(least))
top24.sort(key=lambda ind:sum(ind),reverse=True)
Res=top24[0]
necessary_suppliers=[]
supplier_id=suppliers_scores['Supplier ID'].tolist()
for j,i in enumerate(Res):
    if i==1:
        necessary_suppliers.append(supplier_id[j])
print(f'所需供应商为：{necessary_suppliers}')