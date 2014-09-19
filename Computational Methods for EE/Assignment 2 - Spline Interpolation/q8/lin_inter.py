import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from scipy import weave

def bilinear(orig_base,orig_inter,X,Y,Z,XX,YY):
	print orig_base
	Zs=[]
	h=orig_base[1]-orig_base[0]
	c=np.array(zip(np.ravel(X), np.ravel(Y)))
	for xx,yy in zip(np.ravel(XX), np.ravel(YY)):
		dist=np.sum((c-[xx,yy])**2,axis=1)
		index=np.argmin(dist)
		ind_x1=index%len(X);ind_y1=int(index/len(X))
		
		'''if ind_x1==len(X)-1:
			ind_x2=ind_x1-1
		else:
			ind_x2=ind_x1+1

		if ind_y1==len(Y)-1:
			ind_y2=ind_y1-1
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

		z11=Z[ind_x1][ind_y1];z12=Z[ind_x1][ind_y2];
		z21=Z[ind_x2][ind_y1];z22=Z[ind_x2][ind_y2];
		x1=orig_base[ind_x1];x2=orig_base[ind_x2]
		y1=orig_base[ind_y1];y2=orig_base[ind_y2]

		den=(x2-x1)*(y2-y1)
		num=z11*(x2-xx)*(y2-yy)+z21*(xx-x1)*(y2-yy)+z12*(x2-xx)*(yy-y1)+z22*(xx-x1)*(yy-y1)
		f=num/den;
		Zs=append(Zs,f)
	Z_inter=np.transpose(Zs.reshape(XX.shape))

	return Z_inter

n=5
x=y=linspace(0,1,n)
X,Y=meshgrid(x,y)

zs = np.array([sin(pi*i)*cos(pi*j) for i,j in zip(np.ravel(X), np.ravel(Y))])

Z = zs.reshape(X.shape)

n=50
xx=yy=linspace(0,1,n+1)
XX,YY=meshgrid(xx,yy)

zs = np.array([sin(pi*i)*cos(pi*j) for i,j in zip(np.ravel(XX), np.ravel(YY))])

ZZ = zs.reshape(XX.shape)

Z_inter=bilinear(x,xx,X,Y,Z,XX,YY)

print Z
print ZZ
fig = figure(figsize=(8,6))

# `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
ax = fig.add_subplot(1,1,1, projection='3d')

ax.plot_surface(XX, YY, Z_inter,  alpha=0.25)
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