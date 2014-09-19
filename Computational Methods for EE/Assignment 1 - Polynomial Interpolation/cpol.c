#include<math.h>
#include<stdio.h>

int polint(float xa[],float ya[], int n, float x, float *y, float *dy)
{
	int i,m,ns=0;
	float den, dif, dift, ho,hp,w;
	float c[n],d[n];
	dif=fabs(x-xa[0]);
	for(i=0;i<n;i++)
	{
		if( (dift=fabs(x-xa[i])) < dif)
		{
			ns=i;dif=dift;
		}
		c[i]=ya[i];
		d[i]=ya[i];
	}
	*y=ya[ns];
	for(m=1;m<=n;m++)
	{
		for(i=0;i<n-m;i++)
		{
			ho=xa[i]-x;
			hp=xa[i+m]-x;
			w=c[i+1]-d[i];
			if ( (den=ho-hp) == 0.0) {
				printf("Error in routine polint");
				return 0;
			}
			den=w/den;
			d[i]=hp*den;
			c[i]=ho*den;
		}
		*y += (*dy=(2*ns < (n-m) ? c[ns+1] : d[ns--]) ) ;
		printf("%d %f %d\n",m,*y,ns)	;
	}
	return 1;
}

int main()
{
	float xa[5]={1,2,3,4,5};
	float ya[5]={4,2,1,2,4};
	int n=5;
	float x=2;
	float y, dy;
	polint(xa,ya,n,x,&y,&dy);
	printf("%f %f",y,dy);

}