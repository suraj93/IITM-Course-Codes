#include<stdlib.h>
#include<math.h>

void bcucof(double y[], double y1[], double y2[], double y12[], double d1, 
	double d2,double *c)
{
	static int wt[16][16]=
		{ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
		-3,0,0,3,0,0,0,0,-2,0,0,-1,0,0,0,0,
		2,0,0,-2,0,0,0,0,1,0,0,1,0,0,0,0,
		0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,
		0,0,0,0,-3,0,0,3,0,0,0,0,-2,0,0,-1,
		0,0,0,0,2,0,0,-2,0,0,0,0,1,0,0,1,
		-3,3,0,0,-2,-1,0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,-3,3,0,0,-2,-1,0,0,
		9,-9,9,-9,6,3,-3,-6,6,-6,-3,3,4,2,1,2,
		-6,6,-6,6,-4,-2,2,4,-3,3,3,-3,-2,-1,-1,-2,
		2,-2,0,0,1,1,0,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,2,-2,0,0,1,1,0,0,
		-6,6,-6,6,-3,-3,3,3,-4,4,2,-2,-2,-2,-1,-1,
		4,-4,4,-4,2,2,-2,-2,2,-2,-2,2,1,1,1,1};
	int l,k,j,i;
	double xx,d1d2,cl[16],x[16];
	d1d2=d1*d2;
	for (i=0;i<=3;i++) 
	{
		x[i]=y[i];
		x[i+4]=y1[i]*d1;
		x[i+8]=y2[i]*d2;
		x[i+12]=y12[i]*d1d2;
	}
	for (i=0;i<=15;i++) { 
		xx=0.0;
		for (k=0;k<=15;k++) 
			xx += wt[i][k]*x[k];
		cl[i]=xx;
	}
	l=0;
	for (i=0;i<4;i++) 
	for (j=0;j<4;j++) 
		c[i*4+j]=cl[l++];
}

void bcuint(double y[], double y1[], double y2[], double y12[], double x1l,
double x1u, double x2l, double x2u, double x1, double x2, double *ansy,
double *ansy1, double *ansy2, double *c)
{
	//y--;y1--;y2--;y12--;
	int i;
	double t,u,d1,d2;
	d1=x1u-x1l;
	d2=x2u-x2l;
	bcucof(y,y1,y2,y12,d1,d2,c);
	//if (x1u == x1l || x2u == x2l) 
	//	nrerror("Bad input in routine bcuint");
	t=(x1-x1l)/d1;
	u=(x2-x2l)/d2;
	*ansy=(*ansy2)=(*ansy1)=0.0;
	for (i=3;i>=0;i--) 
	{ 	
		*ansy=t*(*ansy)+((c[i*4+3]*u+c[i*4+2])*u+c[i*4+1])*u+c[i*4+0];
		*ansy2=t*(*ansy2)+(3.0*c[i*4+3]*u+2.0*c[i*4+2])*u+c[i*4+1];
		*ansy1=u*(*ansy1)+(3.0*c[3*4+i]*t+2.0*c[2*4+i])*t+c[1*4+i];
	}
	*ansy1 /= d1;
	*ansy2 /= d2;
}