# script to test the spline routine
from scipy import *
from matplotlib.pyplot import *
from scipy import weave
from scipy.special import jv
def dere(x):
	return (x**(1+jv(0,x))/((1+100*x*x)*(1-x))**0.5)*((1+jv(0,x))/x-jv(1,x)*log(x)-100*x/(1+100*x*x)+1/2/(1-x))

a=0
# define support code
with open("ranint.c","r") as f:
  scode=f.read()
yp1=dere(0.1)
ypn=dere(0.9)
N=100
print N
err=zeros(N)
x=linspace(0.1,0.9,N)
y=x**(1+jv(0,x))/((1+100*x*x)*(1-x))**0.5
n=int(N)
xx=linspace(0.1,0.91,10*n+1)
 # y2=s.spline(x,y,1e31,1e31)
  # yy=s.splintn(x,y,y2,xx)
y2=zeros(xx.size)
c=zeros(xx.size)
d=zeros(xx.size)
yy=zeros(xx.size)
code="""
#include<math.h>  
int i;
double xp;
for(i=0;i<=10*n;i++){
  xp=xx[i];
  ratint(x,y,n,xp,yy+i,y2+i,c,d);
}
"""
weave.inline(code,["x","y","n","y2","xx","yy","c","d"],support_code=scode,extra_compile_args=["-g"],compiler="gcc")
  
zz=[i for i in xx if i<=0.901]
#print zz
dd=yy[:len(zz)]
zz=array(zz)
dd=array(dd)
xx=yy
yy=dd
#if i==0:
figure(0)
plot(x,y,'ro')
print len(xx)
print len(yy)
plot(xx,yy,'g')
title("Interpolated values and data points for n=%d" % N)
figure(2)
plot(xx,abs(yy-(xx**(1+jv(0,xx))/((1+100*xx*xx)*(1-xx))**0.5)),'r')
#figure(3)
#plot(zz,abs(dd-(zz**(1+jv(0,zz))/((1+100*zz*zz)*(1-zz))**0.5)),'r')
#z=abs(yy-(xx**(1+jv(0,xx))/((1+100*xx*xx)*(1-xx))**0.5))
#err[i]=z.max()
#if(err[i]<10**(-6)):
#  if(a==0):
#    print(str(N)+"has the first instance of error tolerance...")
#    a=1
#figure(1)
#plot(N,err)
#title("Plot of error vs No.of points")
show()
