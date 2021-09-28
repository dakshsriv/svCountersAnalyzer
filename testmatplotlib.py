from matplotlib import pyplot as plt
import numpy as np
from pprint import pprint

x = np.arange(0,4)
#y1 = np.array([1,2,4,3])
y1 = [1,2,4,3]
#y2 = np.array([5,2,1,3])
y2 = [5,2,1,3]
pprint(y1)
# y2 should go on top, so shift them up
#y2s = y1+y2

plt.plot(x,y1)
plt.plot(x,y2)
plt.show()