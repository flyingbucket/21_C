import numpy as np
import pandas as pd

"""
决策变量x为50维数组，每一位在1到8的整数中取，表示转运商选择
决策变量y为50维01数组，表示供应商选择
"""
# 读取数据
supplier=pd.read_excel(r'D:\mypython\math_modeling\21_C\data\supply_expectation.xlsx',header=0)
fowarder=pd.read_excel(r'D:\mypython\math_modeling\21_C\data\forwarder_expectation.xlsx',header=0)
fowarder.columns=[i for i in range(25)]
# print(supplier.columns[0])
# print(fowarder.columns[0])

# 成本转换字典
pur_dict=dict(A=1.2,B=1.1,C=1)
to_q_dict=dict(A=1/0.6,B=1/0.66,C=1/0.72)
to_q_dict2=dict(A=0.6,B=0.66,C=0.72)
# 计算采购单价
pur_price_ls=[]
for type in supplier['材料分类'].tolist():
    pur_price_ls.append(pur_dict[type])
pur_price=np.array(pur_price_ls)

to_q_quan1=[]
for type in supplier['材料分类'].tolist():
    to_q_quan1.append(to_q_dict[type])
to_q_quan1=np.array(to_q_quan1)

to_q_quan2=[]
for type in supplier['材料分类'].tolist():
    to_q_quan2.append(to_q_dict2[type])
to_q_quan2=np.array(to_q_quan2)
to_q_price=to_q_quan2*pur_price # to_q_price表示生产单位体积产品的原材料价格

# so far so good---------------


# 函数准备----------------------

def x_ij(i,j):
    '''计算第i个供应商第j周的供应量'''
    return supplier.iloc[i,j+1]
# good

def y_ij(i,j):
    '''计算第i个转运商第j周的损耗率'''
    return fowarder.iloc[i-1,j]
# good

def lose_rate(t):
    '''计算第t周x安排方式下，各转运商的损耗率列表'''
    lose_rate_ls=fowarder[t].tolist()
    lose_rate=[ra/100 for ra in lose_rate_ls]
    return lose_rate
# good

def tell_type(type):
    type_supply=[]
    for Type in supplier['材料分类'].tolist():
        if Type==type:
            type_supply.append(1)
        else:
            type_supply.append(0)
    return np.array(type_supply)

def tell_type_trans(x,i):
    ls=[]
    for tr in x:
        if tr==i:
            ls.append(1)
        else:
            ls.append(0)
    return np.array(ls)

# 目标函数准备---------------------
def pur_cost(y,t):
    '''计算采购成本'''
    pur=[x_ij(i,t) for i in range(50)]
    pur_raw=np.array(pur) # 乘上y即可的本周各供应商供货量
    return np.sum(pur_raw*y*pur_price)

    
def trans_lose(x,y,t):
    '''计算运输损耗'''
    pur_raw=[x_ij(i,t) for i in range(50)]
    pur_raw=np.array(pur_raw)
    lose=lose_rate(t)
    res=0
    for i in lose:
        res+=y*pur_raw*to_q_quan1/np.sum(x)*i
    return res

def new_store(x,y,t,Q):
    '''计算第t周新增库存量'''
    pur_raw=[x_ij(i,t) for i in range(50)]
    pur_raw=np.array(pur_raw) # 乘上y即可的本周各供应商供货量
    lose=lose_rate(t)
    res=0
    for i in lose:
        res+=np.sum(y*pur_raw*to_q_quan1)/np.sum(x)*(1-i)
    return res-Q*10**4

def store(x, y, t, Q,store_history):
    '''计算第t周周末时的库存量'''
    return  store_history[-1] + new_store(x, y, t, Q)

def cost(x,y,t,Q,store_history):
    '''计算第t周周末时的总成本'''
    return pur_cost(y,t)+trans_lose(x,y,t)+store(x,y,t,Q,store_history)

# ---定义目标函数---
def obj(x,y,t,Q,store_history):
    '''目标函数'''
    return cost(x,y,t,Q,store_history)-2*Q*10**4

# ---约束条件---
def trans_con(x,y,t):
    '''转运约束'''
    pur=[x_ij(i,t) for i in range(50)]
    pur_raw=np.array(pur)
    sum=np.sum(y*pur_raw)
    return 6000*np.sum(x)-sum

def store_con(x,y,t,Q,store_history):
    '''库存约束'''
    return store_history[-1]+new_store(x,y,t,Q)-2*Q*10**4

# ---测试---
# x=np.random.randint(1,9,50)
# y=np.random.randint(0,2,50)
# t=1
# pur=[x_ij(i,t) for i in range(50)]
# pur_raw=np.array(pur)
# new=pur_raw*(1-lose_rate_arr(x,t))*y
# store_history=[2*2.82*10**4]
# Q=random.uniform(2.82,5.64)
# A=obj(x,y,t,Q,store_history)
# print(A)