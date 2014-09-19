import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from scipy import weave

with open("spline.c","r") as f:
  scode=f.read()

with open("rationint.c","r") as f:
  rcode=f.read()

def func(x):
	y=(x**(1+jv(0,x)))/(np.sqrt((1+100*(x**2))*(1-x)))
	return y

order=8
n=21
x=linspace(0.1,0.900001,n)
y=func(x)

n1=20000
xx=linspace(0.1,0.900001,n1+1)
yy=zeros(xx.size)
dyy=zeros(xx.size)
c=zeros(x.size)
d=zeros(x.size)

code="""
  #include<stdlib.h>
  #include<math.h>  
  int i;
  double xp;
  for(i=0;i<=n1;i++){
    xp=xx[i];
    rationint(x,y,n,order,xp,yy+i,dyy+i,c,d);
  }
"""

weave.inline(code,["x","y","n","order","n1","xx","yy","dyy","c","d"],support_code=rcode,extra_compile_args=["-g"],compiler="gcc",force=1)

max_err=dyy.max()
print max_err

figure(1)
title('Data Points and Rational Interpolated Values for N=%d' %n)
plot(x,y,'k.')
plot(xx,yy)

figure(2)
title('Rational Interpolation Error and x for N=%d' %n)
semilogy(xx,dyy)
show()