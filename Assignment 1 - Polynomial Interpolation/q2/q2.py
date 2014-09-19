import numpy as np
import pypolint
from matplotlib.pyplot import *

xa=np.linspace(0,1,30)
xb=np.linspace(0,1,5)
ya=np.sin(xa+np.square(xa))
yb=np.sin(xb+np.square(xb))
n=5
xx=np.linspace(-0.5,6.5,1000)
yy=np.sin(xx+np.square(xx))

[y,dy]=pypolint.nearestpolint(xa,ya,n,xx)
[y1,dy1]=pypolint.nearestpolint(xb,yb,n,xx)

figure(1)
plot(xa,ya,'k*',label='Table Values')
plot(xx,y1,'r-',label='5 sample interpolation')
plot(xx,y,'-',label='30 sample interpolation')
xlabel('x')
ylabel('Predicted y values')
legend(loc=3)
figure(2)
gca().set_yscale('log')
plot(xx,abs(y1-yy),'r-',label='5 samples')
plot(xx,abs(y-yy),'-',label='30 samples')
xlabel('x')
ylabel('Error (measured against theoretical value)')
legend(loc=3)
show()
	