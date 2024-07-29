import numpy as np
import pandas as pd

"""
决策变量x为8维01数组，表示转运商选择
决策变量y为50维01数组，表示供应商选择
"""
# 读取数据
supplier=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\supply_expectation.xlsx',header=0)
fowarder=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\forwarder_expectation.xlsx',header=0)
print(supplier.columns[0])
print(fowarder.columns[0])

# 成本转换字典
pur_dict=dict(A=1.2,B=1.1,C=1)
to_q_dict=dict(A=1/0.6,B=1/0.66,C=1/0.72)

# 计算采购单价
pur_price_ls=[]
for type in supplier['材料分类'].tolist():
    pur_price_ls.append(pur_dict[type])
pur_price=np.array(pur_price_ls)

# 计算材料转化率
to_q=[]
for type in supplier['材料分类'].tolist():
    to_q.append(to_q_dict[type])
to_q_rate=np.round(to_q,2)

# so far so good---------------
# 计算损耗率表

def x_ij(i,j):
    '''计算第i个供应商第j周的供应量'''
    return supplier.iloc[i,j+1]

def y_ij(i,j):
    '''计算第i个转运商第j周的损耗率'''
    return fowarder.iloc[i,j]

def trans_rules(x,y,t):
    '''计算第t周的运输规则'''
    return 'hold on'
def pur_cost(y,t):
    '''计算采购成本'''
    pur=[x_ij(i,t) for i in range(50)]
    pur_raw=np.array(pur) # 乘上y即可的本周各供应商供货量
    return np.sum(pur_raw*y*pur_price)

def store(x,y,t):
    '''计算库存量'''
    pur=[x_ij(i,t) for i in range(50)]
    pur_raw=np.array(pur) # 乘上y即可的本周各供应商供货量
    # new=pur_raw*y*
    return 'hold on'
def sto_cost(x,t):
    '''计算库存成本（未考虑转运损耗）'''
    
def lose(x,y,t):
    '''计算转运损耗'''
    return 'hold on'
def trans_cost(x,y,t):
    '''计算运输成本'''
    lose_rate_ls=[y_ij(i,t) for i in range(8)]
    lose_rate=np.array(lose_rate_ls)


    
    