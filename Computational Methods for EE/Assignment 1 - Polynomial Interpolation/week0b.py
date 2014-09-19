from scipy import *
from matplotlib.pyplot import *
import time
import scipy.weave as weave
a=0.5
x=arange(0,3,.1)
# we sum till the Nth term is 1e-4 less than the first.
N=int(max(sqrt(9999)*a,10))
def clenshaw(N,c,x):
    y=zeros((N+3,len(x)))
    F1=cos(x)
    alpha=2*F1
    beta=-ones(x.shape)
    for k in range(N,0,-1):
        y[k,:]=alpha*y[k+1,:] + beta*y[k+2,:] + c[k]
    return(beta*y[2,:] + F1*y[1,:] + c[0])
def fourier(N,c,x):
    z=zeros(x.shape)
    for k in range(N+1):
        z += c[k]*cos(k*x)
    return(z)
def clenc(N,c,x):
    n=len(x)
    y=zeros((N+3,n))
    f=cos(x)
    code = """
    double alpha;
    for( int j=0 ; j<n ; j++ ){
        alpha = 2.0*f[j];
        for( int k=N ; k>0 ; k-- ){
            Y2(k,j)=alpha*Y2(k+1,j)-Y2(k+2,j)+c[k];
        }
        f[j]=-Y2(2,j)+f[j]*Y2(1,j)+c[0];
    }
    """
    weave.inline(code,["y","c","f","N","n"],compiler="gcc")
    return(f)
def fourc(N,c,x):
    n=len(x)
    z=zeros(x.shape)
    code="""
    double xx;
    for( int j=0 ; j<n ; j++ ){
        xx=x[j];z[j]=0;
        for( int k=0 ; k<=N ; k++ )
            z[j] += c[k]*cos(k*xx);
    }
    """
    weave.inline(code,["z","c","x","N","n"],compiler="gcc")
    return(z)
M=1000
nn=arange(N+2)
c=array(1/(nn*nn+a*a))
t1=time.time()
for i in range(M):
    f=clenshaw(N,c,x)
t2=time.time()
py1=(t2-t1)/M
print "Time for clenshaw=%f" % py1
fmax=max(abs(f))
t1=time.time()
for i in range(M):
    fc=clenc(N,c,x)
t2=time.time()
pyc=(t2-t1)/M
print "Time for clenshaw implemented in C=%f" % pyc,
print " (speedup=%f)" % (py1/pyc),
# print relative error with respect to the clenshaw in python.
print " rel err=%e" % (max(abs(f-fc))/fmax)
t1=time.time()
for i in range(M):
    z=fourier(N,c,x)
t2=time.time()
f1=(t2-t1)/M
print "Time for fourier=%f" % f1,
print " rel err=%e" % (max(abs(f-z))/fmax)
t1=time.time()
for i in range(M):
    zz=fourc(N,c,x)
t2=time.time()
f2=(t2-t1)/M
print "Time for fourier in C=%f" % f2,
print " (speedup=%f)" % (f1/f2),
print " rel err=%e" % (max(abs(f-zz))/fmax)
plot(x,f,'bo')
plot(x,z,'k')
plot(x,fc,'r')
plot(x,zz,'g')
title(r"$f=\sum_{k=0}^{%d} \frac{\cos(kx)}{%.2f^2+k^2}$" % (N,a))
show()
