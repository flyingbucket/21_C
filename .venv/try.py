import numpy as np
import pandas as pd
import cvxpy as cp
import tqdm
import warnings

warnings.filterwarnings("ignore")
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
    return cp.sum(y)


def obj2(y):
    '''目标函数2：最大化每周所获得的总分数'''
    total_score = cp.sum(cp.multiply(y, supplier_scores))
    num_selected_suppliers = cp.sum(y)
    res=total_score / num_selected_suppliers if num_selected_suppliers !=0 else 0
    return 1/res if res != 0 else 0  # 取倒数，将目标函数二负向化



def cf(y):
    '''组合目标函数,权重各为50%,越小越好'''
    obj_1 = obj1(y)
    obj_2 = obj2(y)
    return 0.5 * obj_1 + 0.5 * obj_2 

# 定义约束条件
def constraint(y,t):
    x_ls=[x_ij(i,t) for i in range(num_suppliers)]
    x=np.array(x_ls)
    res=np.sum(x*y*con_rate)
    return res-20000
# breakpoint()
least=[]
# for t in tqdm.trange(1,25):
t=1
y = cp.Variable(num_suppliers, boolean=True)
objective = cp.Minimize(cf(y))
constraints = [constraint(y, t) >= 0]
problem = cp.Problem(objective, constraints)
problem.solve()

least.append(sum(y.value))
result_num = max(least)
print(result_num)
print(y.value)
