import numpy as np
import pandas as pd
# a=np.array([1,2,3])
# b=np.zeros(3)
# c=np.vstack((a,b))
# df=pd.DataFrame(c)

# for i in range(3):
#     df.iloc[1,i]=i+1


# print(df)


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
