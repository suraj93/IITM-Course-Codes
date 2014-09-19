
# script to test the spline routine
from scipy import *
from matplotlib.pyplot import *
from scipy import weave
from scipy.special import jv
import ratint
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
x=linspace(0.09,0.92,N)
y=x**(1+jv(0,x))/((1+100*x*x)*(1-x))**0.5
n=int(N)
xx=linspace(0.08,0.92,10*n)
yy=zeros(xx.size)
err=zeros(xx.size)
 # y2=s.spline(x,y,1e31,1e31)
  # yy=s.splintn(x,y,y2,xx)
for i in range(0,len(xx)):
	yy[i],err[i]=ratint.ratint(x,y,xx[i],5)
#if i==0:
zz=[i for i in xx if i<=0.901]
#print zz
dd=yy[:len(zz)]
ee=err[:len(zz)]
zz=array(zz)
dd=array(dd)
ee=array(ee)
xx=zz
yy=dd

zz1=[i for i in xx if i>=0.1]
#print zz
dd=yy[len(zz)-len(zz1):]
ee1=ee[len(zz)-len(zz1):]
zz=array(zz1)
dd=array(dd)
ee1=array(ee1)
xx=array(zz1)
yy=dd


#print len(xx),len(yy),len(ee1)
figure(0)
plot(x,y,'ro')
plot(xx,yy,'g')
title("Interpolated values and data points for n=%d" % N)
figure(2)
yscale('log')
plot(xx,ee1,'r')

figure(3)
yscale('log')
plot(xx,abs(yy-(xx**(1+jv(0,xx))/((1+100*xx*xx)*(1-xx))**0.5)),'r')
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
