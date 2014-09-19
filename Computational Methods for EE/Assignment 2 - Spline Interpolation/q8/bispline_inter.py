import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from scipy import weave

with open("bispline.c","r") as f:
  bcode=f.read()


n=5
x=y=linspace(0,1,n)
X,Y=meshgrid(x,y)

zs = np.array([sin(pi*i)*cos(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)
z=np.array(Z)

zs = np.array([cos(pi*i)*cos(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
ZX = zs.reshape(X.shape)

zs = np.array([-1*sin(pi*i)*sin(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
ZY = zs.reshape(X.shape)

zs = np.array([-1*cos(pi*i)*sin(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
ZXY = zs.reshape(X.shape)

n1=51
xx=yy=linspace(0,1,n1)
XX,YY=meshgrid(xx,yy)

zs = np.array([-1*sin(pi*i)*cos(pi*j) for i,j in zip(np.ravel(XX), np.ravel(YY))])
ZZ = zs.reshape(XX.shape)

Zs=np.zeros(n1*n1)

u=zeros(n)
temp1=zeros(n)
temp2=zeros(n)
ytmp=zeros(n)
yytmp=zeros(n)
z2a=zeros(n*n)
zp=z
values= zp.reshape((n*n,))
print values

code="""
  #include<math.h>  
  #include<stdio.h>
  int i,j,k;
  double xp,yp;
  splie2(x,y,values,n,n,z2a,u,temp1,temp2); 
  for(i=0;i<n1;i++)
  {
  	for(j=0;j<n1;j++)
	  {
      xp=xx[i];
	    yp=yy[j];
	    k=i*n+j;
	    splin2(x,y,values,z2a,n,n,xp,yp,Zs+k,u,temp1,temp2,ytmp,yytmp);
  	}
  }
"""

weave.inline(code,["x","y","values","z2a","n","n1","xx","yy","Zs","u","temp1","temp2","ytmp","yytmp"],support_code=bcode,extra_compile_args=["-g"],compiler="gcc",force=1)

Z_inter=Zs.reshape(XX.shape)


#print Z_inter
#print z2a

fig = figure(figsize=(8,6))

# `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
ax = fig.add_subplot(1,1,1, projection='3d')

ax.plot_surface(XX, YY, Z_inter,  alpha=0.25)
#ax.plot_surface(XX, YY, ZZ,  alpha=0.25)
cset = ax.contour(XX, YY, Z_inter, zdir='z', cmap=cm.coolwarm)
cset = ax.contour(XX, YY, Z_inter, zdir='x', cmap=cm.coolwarm)
cset = ax.contour(XX, YY, Z_inter, zdir='y', cmap=cm.coolwarm)

fig = figure(figsize=(8,6))

# `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
ax = fig.add_subplot(1,1,1, projection='3d')
err=abs(ZZ-Z_inter)
ax.plot_surface(XX, YY, err,  alpha=0.25)
# cset = ax.contour(XX, YY, err, zdir='z', cmap=cm.coolwarm)
# cset = ax.contour(XX, YY, err, zdir='x', cmap=cm.coolwarm)
# cset = ax.contour(XX, YY, err, zdir='y', cmap=cm.coolwarm)

show()