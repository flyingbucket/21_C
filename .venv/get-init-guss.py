import pandas as pd
import numpy as np

order_df = pd.read_excel(r'D:\mypython\math_modeling\21_C\data\order_choice.xlsx',header=0)
trans_df=pd.read_excel(r'D:\mypython\math_modeling\21_C\data\2.xlsx',header=0)

order_df.columns = ['供应商ID','材料分类']+[i for i in range(1,241)]
trans_df.columns = ['转运商ID']+[i for i in range(1,241)]

guess=[]
for i in range(1,241):
    ind_y=order_df[i].tolist()
    ind_x=trans_df[i].tolist()
    for j in range(len(ind_y)):
        if ind_y[j]!=0:
            ind_y[j]=1
        else:
            ind_y[j]=0
    for j in range(len(ind_x)):
        if ind_x[j]!=0:
            ind_x[j]=1
        else:
            ind_x[j]=0
    ind=ind_x+ind_y  #转运商在前，供应商在后
    guess.append(ind)

guess_df=pd.DataFrame(guess)
guess_df.to_excel(r'D:\mypython\math_modeling\21_C\data\guess.xlsx',header=False,index=False)
