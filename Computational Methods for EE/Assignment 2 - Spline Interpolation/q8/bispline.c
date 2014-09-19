#include<stdlib.h>
#include<stdio.h>
#include<math.h>

void spline(double *x,double *y,int n,double yp1,double ypn,double *y2,double *u){
  // It is assumed that x,y,y2 and u have been allocated in the calling program. u is a work array of the same size as x.
  int i,k;
  double p,qn,sig,un;
  x--;y--;y2--;u--; // NR adjustments
  if (yp1 > 0.99e30)
    y2[1]=u[1]=0.0;
  else {
    y2[1] = -0.5;
    u[1]=(3.0/(x[2]-x[1]))*((y[2]-y[1])/(x[2]-x[1])-yp1);
  }
  for (i=2;i<=n-1;i++) {
    sig=(x[i]-x[i-1])/(x[i+1]-x[i-1]);
    p=sig*y2[i-1]+2.0;
    y2[i]=(sig-1.0)/p;
    u[i]=(y[i+1]-y[i])/(x[i+1]-x[i]) - (y[i]-y[i-1])/(x[i]-x[i-1]);
    u[i]=(6.0*u[i]/(x[i+1]-x[i-1])-sig*u[i-1])/p;
  }
  if (ypn > 0.99e30)
    qn=un=0.0;
  else {
    qn=0.5;
    un=(3.0/(x[n]-x[n-1]))*(ypn-(y[n]-y[n-1])/(x[n]-x[n-1]));
  }
  y2[n]=(un-qn*u[n-1])/(qn*y2[n-1]+1.0);
  for (k=n-1;k>=1;k--)
    y2[k]=y2[k]*y2[k+1]+u[k];
  x++;y++;y2++;u++;
}
// still to convert
void splint(double *xa,double *ya,double *y2a,int n,double x,double *y){
  // void nrerror();
  int klo,khi,k;
  double h,b,a;

  xa--;ya--;y2a--; // NR adjustments
  
  klo=1;
  khi=n;
  while (khi-klo > 1) {
    k=(khi+klo) >> 1;
    if (xa[k] > x) khi=k;
    else klo=k;
  }
  h=xa[khi]-xa[klo];
  if (h == 0.0){
    puts("Bad xa input to routine splint");
    exit(1);
  }
  a=(xa[khi]-x)/h;
  b=(x-xa[klo])/h;
  *y=a*ya[klo]+b*ya[khi]+( (a*a*a-a)*y2a[klo]
			   +(b*b*b-b)*y2a[khi] )*(h*h)/6.0;

  xa++;ya++;y2a++; // NR adjustments
}

void splie2(double x1a[], double x2a[], double *ya, int m, int n, double *y2a,double *u,double *temp1,double *temp2)

/*Given an m by n tabulated function ya[1..m][1..n] , and tabulated independent variables
x2a[1..n] , this routine constructs one-dimensional natural cubic splines of the rows of ya
and returns the second-derivatives in the array y2a[1..m][1..n] . (The array x1a[1..m] is
included in the argument list merely for consistency with routine splin2 .)*/

{
//x2a--;ya--;y2a--;
  int i,j;

  for (j=0;j<n;j++)
  {
     for(i=0;i<n;i++)
      {
          temp1[i]=ya[j*n+i];
      } 
      spline(x2a,temp1,n,0,0,temp2,u);
      
      for(i=0;i<n;i++)
      {
          y2a[j*n+i]=temp2[i];
      } 
  }
}

void splin2(double x1a[], double x2a[], double *ya, double *y2a, int m, int n,
double x1, double x2, double *y,double *u,double *temp1,double *temp2,double *ytmp,double *yytmp)

/*Given x1a , x2a , ya , m , n as described in splie2 and y2a as produced by that routine; and
given a desired interpolating point x1 , x2 ; this routine returns an interpolated function value y
by bicubic spline interpolation.*/

{
  int i,j;
  for (j=0;j<m;j++)
  {
    for(i=0;i<n;i++)
      {
          temp1[i]=ya[j*n+i];
          temp2[i]=y2a[j*n+i];
      }
    splint(x2a,temp1,temp2,n,x2,&yytmp[j]);
  }
  spline(x1a,yytmp,m,cos(3.14159*x2),-cos(3.14159*x2),ytmp,u);
  splint(x1a,yytmp,ytmp,m,x1,y);
}