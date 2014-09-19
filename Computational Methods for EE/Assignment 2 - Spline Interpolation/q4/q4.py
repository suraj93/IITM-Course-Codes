import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from scipy import weave

with open("spline.c","r") as f:
  scode=f.read()

def func(x):
	y=(x**(1+jv(0,x)))/(np.sqrt((1+100*(x**2))*(1-x)))
	return y

def func_deriv(x):
	if x==0:
		return 0
	num=np.power(x,1+jv(0,x))
	dnum=num*(-1*jv(1,x)*np.log(x)+(1+jv(0,x))/x)
	den=np.sqrt(1-x+100*(x**2)-100*(x**3))
	dden=(-1+200*x-300*(x**2))/(2*den)
	df=(den*dnum-dden*num)/((den**2))
	return df


flag=0

N=logspace(2,7,20)
max_err=zeros(len(N))
for i in range(len(N)-2):
	n=int(N[i])
	print n
	x=linspace(0.1,0.9,n+1)
	y=func(x)
	yp0=func_deriv(x[0])
	ypend=func_deriv(x[-1])

	n1=10*n
	xx=linspace(0.1,0.9,n1+1)
	y2=zeros(x.size)
	u=zeros(x.size)
	yy=zeros(xx.size)
	code="""
	  #include<math.h>  
	  int i;
	  double xp;
	  spline(x,y,n,yp0,ypend,y2,u); 
	  for(i=0;i<=n1;i++){
	    xp=xx[i];
	    splint(x,y,y2,n,xp,yy+i);
	  }
	"""

	weave.inline(code,["x","y","n","n1","yp0","ypend","y2","u","xx","yy"],support_code=scode,extra_compile_args=["-g"],compiler="gcc")
	
	err=abs(func(xx)-yy)

	if(i==0):
		figure(1)
		plot(x,y,'k.',label='Data Points')
		plot(xx,yy,label='Interpolated Curve')
		title('Data Points and Interpolated Values for N=%d' %n)
		xlabel('x')
		ylabel('f(x)')
		legend(loc=2)
		figure(2)
		semilogy(xx,err)
		title('Interpolation Error and x for N=%d' %n)
		xlabel('x')
		ylabel('Error')
	max_err[i]=err.max()
	if max_err[i] < 10**(-6) and flag==0:
		flag=1
		print 'First 6 digit accurate interpolation is for N=%d' %n
		print xx[1]-xx[0]
		figure(3)
		plot(x,y,'k.',label='Data Points')
		plot(xx,yy,label='Interpolated Curve')
		title('Data Points and Interpolated Values for N=%d' %n)
		xlabel('x')
		ylabel('f(x)')
		legend(loc=2)
		figure(4)
		semilogy(xx,err)
		title('Interpolation Error and x for N=%d' %n)
		xlabel('x')
		ylabel('Error')

figure(5)
loglog(N,max_err,'.-')
title('Plot of Number of Data Points and Max Interpolation Error')
xlabel('Point Spacing')
ylabel('Spline Error')

show()
