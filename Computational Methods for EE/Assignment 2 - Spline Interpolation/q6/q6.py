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

def spacing_generator(tolerance):
	n=10000
	x=linspace(0.1,0.900001,n+1)
	y=func(x)
	dy1=(y[1:]-y[:-1])*n/(0.8)
	dy2=(dy1[1:]-dy1[:-1])*n/(0.8)
	dy3=(dy2[1:]-dy2[:-1])*n/(0.8)
	dy4=(dy3[1:]-dy3[:-1])*n/(0.8)
	mod_x=x[4:]

	precision=0.095

	chunk_bdd=arange(0.1,0.9,precision)
	if chunk_bdd[-1] != 0.9:
		chunk_bdd = append(chunk_bdd,0.9)
	print chunk_bdd
	min_h=zeros(len(chunk_bdd)-1)
	final=[]
	print 'The Optimal Number of points in each Chunk Window Is:'
	for i in range(len(chunk_bdd)-1):
		pointlist=[ n for n,j in enumerate(mod_x) if (j>chunk_bdd[i] and j<=chunk_bdd[i+1]) ]
		first=pointlist[0];last=pointlist[-1]
		max_dy4=max(dy4[first:last])
		min_h[i]=(tolerance*384/(5*max_dy4))**(0.25)

		ext=arange(chunk_bdd[i],chunk_bdd[i+1],min_h[i])
		print '%f - %f & %d' %(chunk_bdd[i],chunk_bdd[i+1],len(ext))
		final.extend(ext)
	#print min_h
	return final


flag=0
print 'Finding Optimal Spacing'
x=spacing_generator(10**(-6))
print 'Interpolating'
x=np.array(x)
y=func(x)
yp0=func_deriv(x[0])
ypend=func_deriv(x[-1])
n=len(x)

n1=100000
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

plot(x,y,'k.')
plot(xx,yy)
title('Data Points and Interpolated Values for N=%d' %n)
figure(2)
semilogy(xx,err)
title('Interpolation Error and x for N=%d' %n)
max_err=err.max()
print max_err
show()
