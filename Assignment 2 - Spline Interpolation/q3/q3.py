import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from scipy import weave

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
	
x=np.arange(0,0.901,0.05)
y=func(x)

dy_first=func_deriv(0)
dy_end=func_deriv(x[-1])
print dy_end

# dy=[func_deriv(xx) for xx in x]
# print dy
# plot(x,dy)
# show()