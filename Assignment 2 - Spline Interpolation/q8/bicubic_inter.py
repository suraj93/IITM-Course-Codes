import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from scipy import weave

with open("bicubic.c","r") as f:
  bcode=f.read()

def bicubic_inter(orig_base,orig_inter,X,Y,Z,ZX,ZY,ZXY,XX,YY):
	print orig_base
	Zs=[]
	v=np.array(zip(np.ravel(X), np.ravel(Y)))
	flag=0
	for xx,yy in zip(np.ravel(XX), np.ravel(YY)):
		# print 'Start'
		dist=np.sum((v-[xx,yy])**2,axis=1)
		index=np.argmin(dist)
		ind_x1=index%len(X);ind_y1=int(index/len(X))
		'''if ind_x1==len(X)-1:
			ind_x2=ind_x1
			ind_x1-=1
		else:
			ind_x2=ind_x1+1

		if ind_y1==len(Y)-1:
			ind_y2=ind_y1
			ind_y1=ind_y1-1
		else:
			ind_y2=ind_y1+1'''

		if xx-orig_base[ind_x1] >=0 and ind_x1<len(X)-1:
			ind_x2=ind_x1+1
		else:
			ind_x2=ind_x1
			ind_x1=ind_x1-1

		if yy-orig_base[ind_y1] >=0 and ind_y1<len(X)-1:
			ind_y2=ind_y1+1
		else:
			ind_y2=ind_y1
			ind_y1=ind_y1-1

		z=np.array([ Z[ind_x1][ind_y1],
						Z[ind_x2][ind_y1],
						Z[ind_x2][ind_y2],
						Z[ind_x1][ind_y2]])
		zx=np.array([ ZX[ind_x1][ind_y1],
						ZX[ind_x2][ind_y1],
						ZX[ind_x2][ind_y2],
						ZX[ind_x1][ind_y2]])
		zy=np.array([ ZY[ind_x1][ind_y1],
						ZY[ind_x2][ind_y1],
						ZY[ind_x2][ind_y2],
						ZY[ind_x1][ind_y2]])
		zxy=np.array([ ZXY[ind_x1][ind_y1],
						ZXY[ind_x2][ind_y1],
						ZXY[ind_x2][ind_y2],
						ZXY[ind_x1][ind_y2]])
		

		x1=orig_base[ind_x1];x2=orig_base[ind_x2]
		y1=orig_base[ind_y1];y2=orig_base[ind_y2]

		zout=np.array([0.0])
		dzout=np.array([0.0])
		ddzout=np.array([0.0])

		code="""
		  #include<stdlib.h>
		  #include<math.h>  
		  double c[]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
		  bcuint(z,zx,zy,zxy,x1,x2,y1,y2,xx,yy,zout,dzout,ddzout,c);
		"""

		
		if not flag:
			weave.inline(code,["z","zx","zy","zxy","x1","x2","y1","y2","xx","yy","zout","dzout","ddzout"],support_code=bcode,extra_compile_args=["-g"],compiler="gcc")
			flag=1
		else:
			weave.inline(code,["z","zx","zy","zxy","x1","x2","y1","y2","xx","yy","zout","dzout","ddzout"],support_code=bcode,extra_compile_args=["-g"],compiler="gcc")
		
		# print zout[0]
		Zs=append(Zs,zout[0])
	Z_inter=np.transpose(Zs.reshape(XX.shape))
	# print len(Zs)
	# print len(XX)

	return Z_inter

n=5
x=y=linspace(0,1,n)
X,Y=meshgrid(x,y)

zs = np.array([sin(pi*i)*cos(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

zs = np.array([cos(pi*i)*cos(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
ZY = zs.reshape(X.shape)

zs = np.array([-1*sin(pi*i)*sin(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
ZX = zs.reshape(X.shape)

zs = np.array([-1*cos(pi*i)*sin(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])
ZXY = zs.reshape(X.shape)

n1=50
xx=yy=linspace(0,1,n1)
XX,YY=meshgrid(xx,yy)

zs = np.array([sin(pi*i)*cos(pi*j) for i,j in zip(np.ravel(XX), np.ravel(YY))])
ZZ = zs.reshape(XX.shape)

Z_inter=bicubic_inter(x,xx,X,Y,Z,ZX,ZY,ZXY,XX,YY)

#print Z
#print ZZ
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