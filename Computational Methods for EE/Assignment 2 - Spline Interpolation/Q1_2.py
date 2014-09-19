import numpy
from scipy import weave
from matplotlib.pyplot import *
'''
def f(x):
	return (x**(1+numpy.sin(x)/x)/(numpy.sqrt(1 - x + 100*x*x -100*x**3)))
'''
with open("spline.c","r") as f:
	scode=f.read()

n=17
x = numpy.linspace(0.1,0.9,n)
y = x**(1+numpy.sin(x)/x)/(numpy.sqrt(1 - x + 100*x*x -100*x**3))
xx = numpy.linspace(0.1,0.9,1000)
yy=numpy.zeros(x.shape) 
#print(x,y)
dy = numpy.zeros(2)
dy[0] = x[0]**(numpy.sin(x[0])/x[0]) * (1 + numpy.sin(x[0])/x[0] -x[0]*(200*x[0]-300*x[0]*x[0]-1)/(2*(1-x[0]+100*x[0]**2-100*x[0]**3)) -x[0]*numpy.log(x[0])*(numpy.sin(x[0])/x[0] - numpy.cos(x[0]))/x[0])/numpy.sqrt(1-x[0]+100*x[0]**2-100*x[0]**3) 
dy[1] = x[16]**(numpy.sin(x[16])/x[16]) * (1 + numpy.sin(x[16])/x[16] -x[16]*(200*x[16]-300*x[16]*x[16]-1)/(2*(1-x[16]+100*x[16]**2-100*x[16]**3)) -x[16]*numpy.log(x[16])*(numpy.sin(x[16])/x[16] - numpy.cos(x[16]))/x[16])/numpy.sqrt(1-x[16]+100*x[16]**2-100*x[16]**3) 
n=17
u=numpy.zeros(x.shape)
y2 = numpy.zeros(x.shape)  
yy=numpy.zeros(xx.shape)
code="""
  #include<math.h>  
  int i;
  double xp;
  spline(x,y,n,dy[0],dy[1],y2,u);
  for(i=0;i<1000;i++){
    xp=xx[i];
    splint(x,y,y2,n,xp,yy+i);
  }
"""
weave.inline(code,["x","y","n","y2","u","xx","yy","dy"],support_code=scode,extra_compile_args=["-g"],compiler="gcc",force=1)
  

plot(x,y)
figure()
print xx
print yy
plot(xx,yy)
show()
