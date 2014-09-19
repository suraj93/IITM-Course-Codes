#include<stdlib.h>
#include<stdio.h>
#include<math.h>

int rationint (double *xa, double *ya, int n, int order, double x, double *y, double *dy, double *c, double *d){
	int m,i,ns=1;
	double w,t,hh,h,dd;
	xa--;ya--;c--;d--;
	hh=fabs(x-xa[1]);
	for(i=1;i<=n;i++){
		h=fabs(x-xa[i]);
		if(h==0.0){
			*y=ya[i];
			*dy=0.0;
			printf("%f:%f\n",x,xa[i]);
			//puts("Bad xa input to routine ratint AAAAAAAA");
			return 1;
		}
		else if (h<hh){
			ns=i;
			hh=h;
		}
		c[i]=ya[i];
		d[i]=ya[i]+1.0e-25;
	}
	*y=ya[ns--];
	int lower, upper;
	lower = ns-order/2;
	upper = ns+order/2+1;
	if(lower<0){
		lower = 0;
		upper = order+1;
	}else if(upper>n){
		upper = n;
		lower = upper-order-1;
	}
	for(m=1;m<n;m++){
		for(i=lower;i<=upper-m;i++){
			w=c[i+1]-d[i];
			h=xa[i+m]-x;
			t=(xa[i]-x)*d[i]/h;
			dd=t-c[i+1];
			if(dd==0.0){
			    puts("Bad xa input to routine ratint BBBBBBB");
			    exit(1);
			}
			dd=w/dd;
			d[i]=c[i+1]*dd;
			c[i]=t*dd;
		}
		*y+=(*dy=(2*ns < (n-m) ? c[ns+1] : d[ns--]));
	}
	return 1;
}

