import numpy as np
a=np.array([1,2,3])
b=np.zeros(3)
c=np.hstack((a,b))
print(c)
print(c[0])