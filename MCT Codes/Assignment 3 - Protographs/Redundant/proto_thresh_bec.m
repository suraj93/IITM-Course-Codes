function [eps]=proto_thresh_bec(A)
    step=0.01;
    Niter=5000;
    count=0;

    for eps=0:step:1
        [x,xmat,status,complete]=proto_de_iter(A,eps,Niter);
        if status==0
            break
        end
    end
    while count<20
        if status ~= 0
            step=step/2;
            eps = eps+step;
        else
            step=step/2;
            eps = eps-step;
        end
        [x,xmat,status,complete]=proto_de_iter(A,eps,Niter);
        count=count+1;
    end    
    if status == 1
        eps=eps+step;
    end
end