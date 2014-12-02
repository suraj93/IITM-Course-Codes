% clear;clc;
% eps=0.48;
% lmax=50;
% rmax=6;
% N=50;
% 

function [y,fval,r] = irreg_opt_single(eps,lmax,rmax,N)
    x=linspace(0,1,N+2);
    x=x(2:end-1);

    ii=2:1:lmax;
    obj_func=(-1)./ii;

    x1=1-(1-x).^(rmax-1);
    xmat=zeros(length(x),length(ii));
    for i=ii
       xmat(1:end,i-ii(1)+1)=eps*x1.^(i-1);
    end
    %xmat(end,:)=[1 zeros(1,length(ii)-1)];

    Aeq=ones(1,length(ii));
    Beq=1;
    lb=zeros(1,length(ii));ub=ones(1,length(ii));

    [y,fval,exitflag,output,lambda]=linprog(obj_func,xmat,x,Aeq,Beq,lb',ub');
    fval=-1*fval;
    fval;
    r=1-1/(rmax*fval);
end