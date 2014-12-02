function [eps] = thresh_finder_bec(lam,rho)
    rho=fliplr(rho);
    lam=fliplr(lam);

    x=0:0.05:1;
    step=0.025;
    count=0;

    r1=polyval(rho,1-x);
    l1=polyval(lam,1-r1);

    for eps=0:0.05:1
        y=eps*l1-x;
        yy=find(y>10^-9);
        if yy > 0
            break
        end
    end
    while length(yy) ~= 1 && count <=10 
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