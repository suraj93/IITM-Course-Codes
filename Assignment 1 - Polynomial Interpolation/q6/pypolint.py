import numpy as np

def polint(xa,ya,n,x):
    diffarr=np.array([(xai-x) for xai in xa])
    diff=min(abs(diffarr))
    ns=np.where(abs(diffarr)==diff)[0][0]
    c=np.array(ya)
    d=np.array(ya)
    y=ya[ns]
    for m in range(1,(n)):
        ho=diffarr[0:n-m]
        hp=diffarr[m:n]
        # print c
        # print d
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


    if abs(diff) <1:
        if diff<=0.5:
            lower=ns-np.floor((n-1)/2)-1
            upper=ns+np.ceil((n)/2)-1
        else:
            lower=ns-np.floor((n-1)/2)
            upper=ns+np.ceil((n)/2)
    else:
        lower=ns-np.floor((n-1)/2)
        upper=ns+np.ceil((n)/2)

    if lower<0:
        upper+=(-1*lower)
        lower=0
    elif upper>(len_diffarr-1):
        lower-=(upper-len_diffarr+1)
        upper=len_diffarr-1
    upper+=1
    return [int(lower),int(upper)]

def nearestpolint(xa,ya,n,xx):
    y=np.zeros_like(xx)
    dy=np.zeros_like(xx)
    for i in range(0,len(xx)):
        x=xx[i]
        [lower,upper]=findnearest(xa,n,x)
        [y[i],dy[i]]=polint(xa[lower:upper],ya[lower:upper],n,x)
    return [y,dy]

# xa=[1,2,3,4,5];
# ya=[1,2,3,2,1];
# n=5;
# x=1.2
# [lower,upper] = findnearest(xa,n,x)
# print xa[lower:upper]
# print ya[lower:upper]
# [y,dy]=polint(xa[lower:upper],ya[lower:upper],n,x)
# print y
# print dy