# script to test the spline routine
from scipy import *
from matplotlib.pyplot import *
from scipy import weave
from scipy.special import jv

a=0
# define support code
with open("spline.c","r") as f:
  scode=f.read()

N=arange(100,500000,10000)
err=zeros(N.shape)
for i in range(N.shape[0]):
  x=linspace(0.1,0.9,N[i])
  y=x**(1+jv(0,x))/((1+100*x*x)*(1-x))**0.5
  n=int(N[i])
  xx=linspace(0.1,0.9,10*n+1)
  # y2=s.spline(x,y,1e31,1e31)
  # yy=s.splintn(x,y,y2,xx)
  y2=zeros(x.size)
  u=zeros(x.size)
  yy=zeros(xx.size)
  code="""
  #include<math.h>  
  int i;
  double xp;
  spline(x,y,n,0,0,y2,u);
  for(i=0;i<=10*n;i++){
    xp=xx[i];
    splint(x,y,y2,n,xp,yy+i);
  }
"""
  weave.inline(code,["x","y","n","y2","u","xx","yy"],support_code=scode,extra_compile_args=["-g"],compiler="gcc")
  
  if i==0:
    figure(0)
    plot(x,y,'ro')
    plot(xx,yy,'g')
    title("Interpolated values and data points for n=%d" % N[i])
    figure(2)
    xlabel('x')
    ylabel('Error')
    plot(xx,abs(yy-(xx**(1+jv(0,xx))/((1+100*xx*xx)*(1-xx))**0.5)),'r')
    title("Error with x for n=%d" % N[i])
  z=abs(yy-(xx**(1+jv(0,xx))/((1+100*xx*xx)*(1-xx))**0.5))
  err[i]=z.max()
  if(err[i]<10**(-6)):
    if(a==0):
      print(str(N[i])+"has the first instance of error tolerance...")
      a=1
figure(1)
loglog(N,err)
title("Plot of error vs No.of points on log log scale")
show()
