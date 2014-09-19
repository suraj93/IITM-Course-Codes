import numpy as np
import pypolint
from matplotlib.pyplot import *

xa=np.linspace(0,1,30)
ya=np.sin(xa+np.square(xa))
xx=np.linspace(-0.5,1.5,600)
yy=np.sin(xx+np.square(xx))


n=5
[y1,dy1]=pypolint.nearestpolint(xa,ya,n,xx)

n=8
[y2,dy2]=pypolint.nearestpolint(xa,ya,n,xx)

n=12
[y3,dy3]=pypolint.nearestpolint(xa,ya,n,xx)

figure(1)
plot(xa,ya,'g*',label='Table Values')
plot(xx,y1,'-',label='4th order interpolation')
plot(xx,y2,'r-',label='7th order interpolation')
plot(xx,y3,'k-',label='11th order interpolation')
xlabel('x')
ylabel('Predicted y values')
legend(loc=3)


figure(2)
gca().set_yscale('log')
plot(xx,abs(y1-yy),'b-',label='4th order interpolation')
plot(xx,abs(y2-yy),'r-',label='7th order interpolation')
plot(xx,abs(y3-yy),'k-',label='11th order interpolation')
xlabel('x')
ylabel('Error (measured against theoretical value)')
legend(loc=4)

# figure(3)
# gca().set_yscale('log')
# plot(xx,abs(dy1),'b-',label='4th order interpolation')
# plot(xx,abs(dy2),'r-',label='7th order interpolation')
# plot(xx,abs(dy3),'k-',label='11th order interpolation')
# xlabel('x')
# ylabel('Error (from polint)')
# legend(loc=9)
show()
	