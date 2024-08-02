import numpy as np
import pandas as pd

supply=pd.read_excel(r'D:\mypython\math_modeling\21_C\data\order_choice.xlsx',header=0)
supplier=supply['供应商ID'].values.tolist()
sup_arr=np.array(supplier)
# print(supplier)
dfx=pd.read_excel(r'D:\mypython\math_modeling\21_C\result\Q4_result.xlsx',sheet_name='x',header=None)
dfy=pd.read_excel(r'D:\mypython\math_modeling\21_C\result\Q4_result.xlsx',sheet_name='y',header=None)

DF=pd.DataFrame()
for w in range(24):
    name='w'+str(w+1)
    x=dfx.loc[w].values.tolist()
    y=dfy.loc[w].values.tolist()
    x_arr=np.array(x)
    for i in range(50):
        if y[i]==0:
            continue
        else:
            y[i]=1
    y_arr=np.array(y)
    trans=x_arr*y_arr
    trans_ls=trans.tolist()
    sel=y_arr*sup_arr
    sel_ls=sel.tolist()
    supply_ls=[s for s in sel_ls if s!=0]
    trans_ls=[t for t in trans_ls if t!=0]
    S=np.array(supply_ls)
    T=np.array(trans_ls)
    res=np.vstack((S,T))
    res = pd.DataFrame(res.T, columns=['供应商ID', '转运商ID'])
    DF = pd.concat([DF, res], axis=1)
DF.to_excel(r'D:\mypython\math_modeling\21_C\result\result4.xlsx',index=False)




