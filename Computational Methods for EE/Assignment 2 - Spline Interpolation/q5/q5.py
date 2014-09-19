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

N=logspace(2,5,15)
max_err=zeros(len(N))
max_err_old=zeros(len(N))
l=0
pl=[]
k=np.array([0,0,0,0,0])
for i in range(len(N)):
	n=int(N[i])
	x=linspace(0.1,0.900001,n+1)
	y=func(x)
	yp0=func_deriv(x[0])
	ypend=func_deriv(x[-1])
	yp0=100*yp0
	ypend=100*ypend

	n1=10*n
	xx=linspace(0.1,0.900001,n1+1)
	
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


	code="""
	  #include<math.h>  
	  int i;
	  double xp;
	  spline(x,y,n,yp0,ypend,y2_old,u); 
	  for(i=0;i<=n1;i++){
	    xp=xx[i];
	    splint(x,y,y2_old,n,xp,yy_old+i);
	  }
	"""

	y2_old=zeros(x.size)
	u=zeros(x.size)
	yy_old=zeros(xx.size)
	yp0=yp0/100.0
	ypend=ypend/100.0


	weave.inline(code,["x","y","n","n1","yp0","ypend","y2_old","u","xx","yy_old"],support_code=scode,extra_compile_args=["-g"],compiler="gcc")
	
	err_old=abs(func(xx)-yy_old)
	

	if(i==0):
		figure(1)
		plot(x,y,'k.')
		plot(xx,yy,label='Original Derivative')
		plot(xx,yy_old,'r',label='100x Derivative')
		title('Data Points and Interpolated Values for N=%d' %n)
		legend(loc=9)
		figure(2)
		semilogy(xx,err,label='Original Derivative')
		semilogy(xx,err_old,'r',label='100x Derivative')
		title('Interpolation Error and x for N=%d' %n)
		legend(loc=9)
	max_err[i]=err.max()
	max_err_old[i]=err_old.max()
	if max_err[i] < 10**(-6) and flag==0:
		flag=1
		print 'First 6 digit accurate interpolation is for N=%d' %n
	if i==0 or i%3==0:
		figure(4)
		index=[ n for n,j in enumerate(xx) if j>0.85 ][0]
		print int(N[i])
		plx=semilogy(xx[index:],err[index:])
		pl.extend(plx)
		
figure(4)
legend(pl,['100','439','1930','8483','37275'],loc=6)
xlabel('x')
ylabel('Error')

figure(3)
loglog(N,max_err_old,'r.-',label='Original Derivative')
loglog(N,max_err,'.-',label='100x Derivative')
title('Plot of Number of Data Points and Max Interpolation Error')
xlabel('No of Points')
ylabel('Spline Error')
legend()




show()
