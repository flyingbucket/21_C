import multiprocessing
from init2_run_p1 import run_p1
from init2_run_p2 import run_p2
from tqdm import trange
import json

def run_part(start, end, current_space, part_number):
    for j in trange(start, end):
        i = start - 1
        current_space = run_p2(i, j, current_space)
    for i in trange(start, end):
        j = start
        current_space = run_p2(i, j, current_space)
    with open(rf'I:\AAA\dev3\data\search_space{part_number}.txt', 'w') as file:
        json.dump(current_space, file)
    return current_space

if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    current_space=run_p1()
    for part_number in range(1, 10):
        current_space = run_part(part_number, part_number + 1, current_space, part_number)

        


    
    
    

