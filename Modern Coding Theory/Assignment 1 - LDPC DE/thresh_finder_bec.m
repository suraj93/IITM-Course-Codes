% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Function to find the BEC threshold of an LDPC code, given 
%               the degree distributions
%
% Author      : Surajkumar Harikumar (EE11B075)

function [eps] = thresh_finder_bec(lam,rho)
    rho=fliplr(rho);
    lam=fliplr(lam);

    step=0.01;
    x=0:2*step:1;
    count=0;

    r1=polyval(rho,1-x);
    l1=polyval(lam,1-r1);

    for eps=0:2*step:1
        y=eps*l1-x;
        yy=find(y>10^-9);
        if yy > 0
            break
        end
    end
    while length(yy) ~= 1 && count <=20
        yy_prev = yy;
        if length(yy)==0
            if length(yy_prev) == 0
                step=step/2;
            end
            eps = eps+step;
        elseif length(yy) > 1
            if length(yy_prev) == 0
                step=step/2;
            end
            eps=eps-step;
        end
        y=eps*l1-x;
        yy=find(y>10^-9);
        count=count+1;
    end   
    
end