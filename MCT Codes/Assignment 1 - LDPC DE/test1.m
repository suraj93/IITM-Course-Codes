% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Script to find best degree distribution using irreg_opt_single 
%               and computing its threshold using thresh_finder_bec     
%
% Author      : Surajkumar Harikumar (EE11B075)

clear;clc;
eps=0.48;
lmax=100;
rmax=12;
N=500;
rate_max=0;
rho_max=3;

% [lam_max,fval,rate] = irreg_opt_single(eps,lmax,rmax,N);
% rho_max=rmax;

for i=3:rmax
    i
    [lam1,fval,rate] = irreg_opt_single(eps,lmax,i,N);
    if rate > rate_max
        
        c=find(lam1>10^(-9));
        lam1=lam1(1:c(end));
        
        rate_max=rate;
        lam_max=lam1;
        rho_max=i;
    end
end

lam=[0 lam_max'];
rho=[ zeros(1,rho_max-1) 1];
eps_calc = thresh_finder_bec(lam,rho)

1-eps_calc
rate_max