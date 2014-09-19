import numpy as np
import pypolint
from matplotlib.pyplot import *

def fx(xa):
	a1=np.sqrt(1-np.square(xa))
	a2=np.sin(np.pi*xa)
	ya=a2/a1
	return ya
	
interval=0.025
xa=np.arange(0.1,0.9001,interval)
ya=fx(xa)

xx=np.linspace(0.1,0.9001,1000)
yy=fx(xx)
n=7
[y,dy]=pypolint.nearestpolint(xa,ya,n,xx)

figure(1)
plot(xx,yy,'g-')
plot(xx,y,'-')

figure(2)
gca().set_yscale('log')
plot(xx,abs(y-yy))


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