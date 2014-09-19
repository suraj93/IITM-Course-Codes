import numpy as np
import pypolint
from matplotlib.pyplot import *

def fx(xa):
	a1=np.sqrt(1-np.square(xa))
	print 1/a1
	a2=np.sin(np.pi*xa)
	print a2
	ya=a2/a1
	return ya
	
interval=0.001
xa=np.arange(0.001,0.991,interval)
ya=fx(xa)

figure(1)
plot(xa,ya,'g-')

dya=(ya[1:]-ya[:-1])/interval

figure(2)
plot(xa[:-1],dya,'g-')


d2ya=(dya[1:]-dya[:-1])/interval

figure(3)
plot(xa[:-2],d2ya,'g-')


d3ya=(d2ya[1:]-d2ya[:-1])/interval

figure(4)
plot(xa[:-3],abs(d3ya),'g-')

d4ya=(d3ya[1:]-d3ya[:-1])/interval

#Fourth derivative is not continuous ? => Not analytic ?
figure(5)
plot(xa[:-4],d4ya,'g-')


d5ya=(d4ya[1:]-d4ya[:-1])/interval

figure(6)
gca().set_yscale('log')
plot(xa[:-5],d5ya,'g-')

d6ya=(d5ya[1:]-d5ya[:-1])/interval

figure(7)
gca().set_yscale('log')
plot(xa[:-6],abs(d6ya),'g-')

show()	


# xx=np.linspace(0,2*pi,999)
# yy=fx(xx)
# maxdy=np.zeros(18)
# for n in range(3,21):
# 	print n
# 	[y,dy]=pypolint.nearestpolint(xa,ya,n,xx)
# 	maxdy[n-3]=max(abs(y-yy))

# print maxdy



# figure(0)
# plot(xx[0:500],yy[0:500],'g-')
# plot(xx[0:500],y[0:500],'-')

# figure(1)
# plot(xx,yy,'g-')
# plot(xx,y,'-')

# figure(2)
# gca().set_yscale('log')
# plot(xx,abs(y-yy))

# show()



'''dy=np.array(ya)
for m in range(1,3):
	dy=(dy[1:]-dy[0:-1])*101

#plot(xa[0:-m],dy)

plot(xa,ya)
show()
'''