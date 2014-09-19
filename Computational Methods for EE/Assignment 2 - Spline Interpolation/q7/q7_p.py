import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from scipy import weave
import ratint_new as ratint

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

order=7
n=101
x=linspace(0.1,0.901,n)
y=func(x)
yp0=func_deriv(x[0])
ypend=func_deriv(x[-1])

n1=10*n
xx=linspace(0.101,0.8901,n1)	
yy=func(xx)
y_inter_1=zeros(xx.size)
y_inter_2=zeros(xx.size)
y_inter_3=zeros(xx.size)
err=zeros(xx.size)

for i in range(0,len(xx)):
	y_inter_1[i],err[i]=ratint.ratint(x,y,xx[i],order)

order=8
for i in range(0,len(xx)):
	y_inter_2[i],err[i]=ratint.ratint(x,y,xx[i],order)


order=19
for i in range(0,len(xx)):
	y_inter_3[i],err[i]=ratint.ratint(x,y,xx[i],order)

figure(0)
plot(x,y,'.')
plot(xx,y_inter_1,'g')
title("Interpolated values and data points for order=%d" % order)
figure(3)
semilogy(xx,abs(yy-y_inter_1),'k',label='7th-order')
semilogy(xx,abs(yy-y_inter_2),'b',label='8th-order')
semilogy(xx,abs(yy-y_inter_3),'r',label='19th-order')
legend(loc=9)
xlabel('x')
ylabel('Error')
show()