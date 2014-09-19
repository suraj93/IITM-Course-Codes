
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
	len_diffarr=len(dd)
	dif=min(dd)
	ns=np.where( dd==dif )[0][0]
	y=ya[ns]
	q=np.array([0.]*order)
	error=0.0
#	print "Order = "+str((order+1)/2)
	if dif<=0.5:
		lower=ns-np.floor((order-1)/2)-1
		upper=ns+np.ceil((order)/2)-1
	else:
		lower=ns-np.floor((order-1)/2)
		upper=ns+np.ceil((order)/2)
	if lower<0:
		upper+=(-1*lower)
		lower=0
	elif upper>(len_diffarr-1):
		lower-=(upper-len_diffarr+1)
		upper=len_diffarr-1
	upper+=1

	
	s=lower
	e=upper
	p=ya[s:e]
	f=xa[s:e]
	if((order+1) >= ya.shape[0]):
#		print "not suffiecent data"
		p=ya
		f=xa

	n=order-1
	ns=ns-s-1
#	print len(f),len(p)
	c=np.array(p)
	d=np.array(p)
	for m in range(1,n):
		# print m
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
			# print x
			# print ns
			# print '\n'
			dy=d[ns]
		y+=dy
	return y,abs(dy)

# Plotting

