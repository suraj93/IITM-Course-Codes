import numpy as np

def polint(xa,ya,n,x):
    diffarr=np.array([(xai-x) for xai in xa])
    diff=min(abs(diffarr))
    ns=np.where(abs(diffarr)==diff)[0][0]
    c=np.array(ya)
    d=np.array(ya)
    y=ya[ns]
    for m in range(1,(n-1)):
        ho=diffarr[0:n-m]
        hp=diffarr[m:n]
        w=c[1:n-m+1]-d[0:n-m]
        den=ho-hp
        den=w*(1./den)
        c=ho*den
        d=hp*den
        if 2*ns < n-m:
            dy=c[ns]
        else:
            ns-=1
            dy=d[ns]
        y+=dy
        # print "%d %f %d %d" %(m,y,ns,n-m)

    return [y,dy]

def findnearest(xa,n,x):
    diffarr=np.array([(xai-x) for xai in xa])
    len_diffarr=len(diffarr)
    diff=min(abs(diffarr))
    ns=np.where(abs(diffarr)==diff)[0][0]
    lower=ns-np.ceil((n-1)/2)
    upper=ns+np.floor((n-1)/2)
    if lower<0:
        upper+=(-1*lower)
        lower=0
    elif upper>=(len_diffarr-1):
        lower-=(upper-len_diffarr+1)
        upper=len_diffarr-1
    upper+=1
    return [int(lower),int(upper)]




# xa=[1,2,3,4,5,6,7,8];
# ya=[3,3,4,6,6,7,8,9];
# n=5;
# x=5.5;
# [lower,upper] = findnearest(xa,n,x)
# xa=xa[lower:upper]
# ya=ya[lower:upper]
# [y,dy]=polint(xa,ya,n,x)
# print y
# print dy