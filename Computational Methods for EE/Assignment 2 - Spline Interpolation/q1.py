import numpy as np
from scipy.special import jn,jv
from matplotlib.pyplot import *

x=np.arange(0,0.901,0.05)
y=(x**(1+jv(0,x)))/(np.sqrt((1+100*(x**2))*(1-x)))
print y
plot(x,y)
show()