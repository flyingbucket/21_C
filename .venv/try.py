import numpy as np
import pandas as pd
# a=np.array([1,2,3])
# b=np.zeros(3)
# c=np.vstack((a,b))
# df=pd.DataFrame(c)

# for i in range(3):
#     df.iloc[1,i]=i+1


# print(df)

'''
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
x=np.random.randint(0,9,size=50)
y=np.random.randint(0,2,size=50)
ind=np.hstack((x,y))

print(check(ind))
'''
'''
a=0
if a:
    print("a is true")
else:
    print("a is false")
'''
# b=0
# for i in range(10):
#     b=i
# print(b)
# 


import random
import json
from deap import base, creator, tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_int", np.random.randint, 1, 9,size=50)
toolbox.register("attr_bool", np.random.randint, 0, 2,size=50)
toolbox.register("con_xy",lambda: np.hstack((toolbox.attr_int(), toolbox.attr_bool())).tolist())
toolbox.register("individual", lambda:creator.Individual(toolbox.con_xy()))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

population = toolbox.population(n=2400)
with open(r'D:\mypython\math_modeling\21_C\data\search_space.txt', 'w') as file:
    json.dump(population, file)

with open(r'D:\mypython\math_modeling\21_C\data\search_space.txt', 'r') as file:
    search_space = json.load(file)

toolbox.register("individual", lambda:creator.Individual(random.choice(search_space)))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def myfunc(v1,v2,toolbox,v3):
    # myfunc计算代码,v1,v2,v3需要动态传入，
    # toolbox是deap提供的工具箱，已经定义好，要保持不变
    return res
result=pool.starmap(myfunc,[(1,2,3,toolbox) for _ in range(10)])