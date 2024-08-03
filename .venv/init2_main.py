import multiprocessing
from init2_run_p1 import run_p1
from init2_run_p2 import run_p2
from tqdm import trange
import json

if __name__ == '__main__':
    multiprocessing.freeze_support()
    current_space=run_p1()
    for j in trange (1,6):
        i=0
        current_space=run_p2(i,j,current_space)
    for i in trange (1,6):
        j=5
        current_space=run_p2(i,j,current_space)
    with open(r'I:\AAA\dev3\data\search_space.txt', 'w') as file:
            json.dump(current_space, file)