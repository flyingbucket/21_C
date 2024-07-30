import pandas as pd
import numpy as np

dfx=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\GA_x.xlsx')
dfy=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\GA_y.xlsx')
dfc=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\GA_cost.xlsx')
supplier_df=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\supply_expectation.xlsx')
forwarder_df=pd.read_excel(r'D:\mypython\math_modeling\21_C\.venv\forwarder_expectation.xlsx')

supplier=supplier_df['供应商ID'].tolist()
forwarder=forwarder_df['转运商ID'].tolist()

# print(dfy.loc[0])
for j in range(24):
    for i in range(50):
        dfx.iloc[j,i]=dfx.iloc[j,i]*dfy.iloc[j,i]
for j in range(24):
    for i in range(50):
        dfy.iloc[j,i]=dfy.iloc[j,i]*supplier[i]


dfx.to_excel(r'D:\mypython\math_modeling\21_C\.venv\GA_x_supply.xlsx',index=False)
dfy.to_excel(r'D:\mypython\math_modeling\21_C\.venv\GA_y_supply.xlsx',index=False)