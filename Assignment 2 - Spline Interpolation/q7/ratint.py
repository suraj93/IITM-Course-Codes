# script to test the spline routine
from scipy import *
from matplotlib.pyplot import *
from scipy import weave
from scipy.special import jv
from numpy import *

def ratint(xa,ya,x,order):
	order=order+1
	# define support code
# interpolation initialization
	dd=np.array([0.]*len(xa))
	dd[:]=abs(xa[:] - x)
	dif=min(dd)
	ns=np.where( dd==dif )[0][0]
	y=ya[ns]
	q=np.array([0.]*order)
	error=0.0
#	print "Order = "+str((order+1)/2)
	e=ns+int((order+3)/2)
	s=ns-int((order+1)/2)
	if(s<0):
#		print "start before 0"
		s=0
		e=order+1
	if(e>ya.shape[0]):
#		print "End after last element"
		s=ya.shape[0]-order-1
		e=ya.shape[0]
	p=ya[s:e]
	f=xa[s:e]
	if((order+1) >= ya.shape[0]):
#		print "not suffiecent data"
		p=ya
		f=xa

	n=order+1
	ns=ns-s
#	print len(f),len(p)
	c=np.array(p)
	d=np.array(p)
	for m in range(1,n):
		w=c[1:n-m+1]-d[0:n-m]
		h=f[m:n]-f[0:n-m]
		t=(f[:n-m]-x)*d[:n-m]/h
		dd=t-c[1:n-m+1]
		dd=w/dd
		d=c[1:n-m+1]/dd
		c=t*dd
		if 2*ns < n-m:
			dy=c[ns]
		else:
			ns-=1
			dy=d[ns]
		y+=dy
	return y,abs(dy)

# Plotting

