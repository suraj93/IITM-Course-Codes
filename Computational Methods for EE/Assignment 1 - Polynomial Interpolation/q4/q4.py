import numpy as np
import pypolint
from matplotlib.pyplot import *

pi=np.pi
xa=np.linspace(-pi,pi,101)
ya=np.zeros_like(xa)
for i in range(1,6):
	j=2*i+1
	ya=ya+np.sin(j*xa)/j

dy=np.array(ya)
for m in range(1,7):
	dy=(dy[1:]-dy[0:-1])*101

figure(1)
plot(xa,ya,'.-')
title('Function Plot')
figure(2)
plot(xa[0:-m],dy)
title('6th derivative of function')
show()