import numpy as np
import pypolint
from matplotlib.pyplot import *

xa=np.linspace(0,1,5)
ya=np.sin(xa+np.square(xa))
n=5
xx=np.linspace(-0.5,1.5,200)
yy=np.sin(xx+np.square(xx))

[y,dy]=pypolint.nearestpolint(xa,ya,n,xx)

figure(1)
plot(xa,ya,'k*',label='Theoretical Values')
plot(xx,y,'-',label='4th order interpolation')
xlabel('x')
ylabel('Predicted y values')
legend(loc=3)
figure(2)
gca().set_yscale('log')
plot(xx,abs(y-yy),'-')
xlabel('x')
ylabel('Error (measured against theoretical value)')
show()

	