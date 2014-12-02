% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Script to find the BEC Area threshold of Spatially Coupled
%               protograph LDPC codes, given the bit and check node
%               degrees. 
%               The threshold is found using the the potential function. 
%               Also plots the potential function for various values of the 
%               channel paramter.
%
% Author      : Surajkumar Harikumar (EE11B075)

clear;clc;

lam_degree = 3; rho_degree=6;

lam = [ zeros(1,lam_degree-1) 1 ] ;
rho = [ zeros(1,rho_degree-1) 1 ] ;
rho_d = [ zeros(1,rho_degree-2) rho_degree-1];

z=0:0.0005:1;
eps_list=0:0.001:1;
for i=1:length(eps_list)
    eps=eps_list(i);
    U_inner = polyval(fliplr(rho_d),1-z).*(z - eps*(polyval(fliplr(lam),(1 - polyval(fliplr(rho),1-z) ) ) ));
    Y=cumtrapz(z,U_inner);
    s=sum(Y<0);
    if s > 0
        break
    end
end
count=0;
inc=eps_list(2)-eps_list(1);
while count<20
        inc=inc/2;
        if s > 0
            eps = eps-inc;
        else
            eps = eps+inc;
        end
        U_inner = polyval(fliplr(rho_d),1-z).*(z - eps*(polyval(fliplr(lam),(1 - polyval(fliplr(rho),1-z) ) ) ));
        Y=cumtrapz(z,U_inner);
        s=sum(Y<0);
        count=count+1;
end    

eps_old=proto_thresh_bec_brute([lam_degree,lam_degree]);
U_old=polyval(fliplr(rho_d),1-z).*(z - eps_old*(polyval(fliplr(lam),(1 - polyval(fliplr(rho),1-z) ) ) ));
Y_old=cumtrapz(z,U_old);

eps
eps_old

eps_h=0.5;
U_h=polyval(fliplr(rho_d),1-z).*(z - eps_h*(polyval(fliplr(lam),(1 - polyval(fliplr(rho),1-z) ) ) ));
Y_h=cumtrapz(z,U_h);

ex1=strcat({'Area Threshold - '},num2str(eps));
ex2=strcat({'BP Threshold - '},num2str(eps_old));
ex3=strcat({'Channel Parameter - '},num2str(eps_h));

figure(1);
plot(z,Y_old,'r-');
hold on;
plot(z,Y,'b-');
plot(z,Y_h,'g-');
plot([0,1],[0,0],'k-');
xlabel('X');
ylabel('U(X)');
legend([ex1,ex2,ex3]);
