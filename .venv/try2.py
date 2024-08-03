import random
import json

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
with open(r'D:\mypython\math_modeling\21_C\data\search_space.txt', 'r') as file:
    search_space = json.load(file)

toolbox.register("individual", lambda:creator.Individual(random.choice(search_space)))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
pop=toolbox.population(n=3)
print(type(pop))
ind=pop[0]
print(type(ind))
print(len(ind))
print(ind)


# # 创建适应度最小化类型
# creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMin)