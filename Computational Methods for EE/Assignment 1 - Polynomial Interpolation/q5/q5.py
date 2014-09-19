import numpy as np
import pypolint
from matplotlib.pyplot import *

def fx(xa):
	ya=np.zeros_like(xa)
	for i in range(1,6):
		j=2*i+1
		ya=ya+np.sin(j*xa)/j
	return ya

pi=np.pi
xa=np.linspace(-pi,pi+0.0001,101)
ya=fx(xa)

xx=np.linspace(0,2*pi,999)
yy=fx(xx)

n=6
[y,dy]=pypolint.nearestpolint(xa,ya,n,xx)

figure(0)
title('Function Comparison in (0,pi)')
plot(xx[0:500],yy[0:500],'g-',label='Theoretical Value')
plot(xx[0:500],y[0:500],'-',label='5th order interpolation')
xlabel('x')
ylabel('f(x)') 
legend(loc=9)

figure(1)
title('Function Comparison in (0,2*pi)')
plot(xx,yy,'g-',label='Theoretical Value')
plot(xx,y,'-',label='5th order interpolation')
xlabel('x')
ylabel('f(x)')
legend()

figure(2)
title('Magnitude of Interpolation Error (semilogy plot)')
gca().set_yscale('log')
plot(xx,abs(y-yy))
xlabel('x')
ylabel('Error')

show()



'''dy=np.array(ya)
for m in range(1,3):
	dy=(dy[1:]-dy[0:-1])*101

#plot(xa[0:-m],dy)

plot(xa,ya)
show()
'''