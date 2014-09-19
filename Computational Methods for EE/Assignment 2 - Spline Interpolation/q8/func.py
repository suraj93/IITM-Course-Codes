import numpy as np
from scipy.special import jn,jv
from scipy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from scipy import weave

x=linspace(0,1,5)
X, Y = np.mgrid[0:1:5j, 0:1:5j]
Z=sin(pi*X)*cos(pi*Y)

fig = figure(figsize=(8,6))

# `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
ax = fig.add_subplot(1,1,1, projection='3d')

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.25)
cset = ax.contour(X, Y, Z, zdir='z', cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='x', cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='y', cmap=cm.coolwarm)

ax.set_xlim3d(0, 1);
ax.set_ylim3d(0, 1);
ax.set_zlim3d(-1, 1);

show()