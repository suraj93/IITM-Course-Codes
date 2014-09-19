import numpy as np
import pypolint
from matplotlib.pyplot import *

xa=[1,2,3,4,5,6];
ya=[1,2,3,2,1,0];
n=6;
xx=np.linspace(1.0,6.0,200)

[y,dy]=pypolint.nearestpolint(xa,ya,n,xx)

figure(1)
plot(xx,y)
show()