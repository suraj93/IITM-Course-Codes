% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Function to find the BEC threshold of a protograph, given 
%               the base parity check matrix
%
% Author      : Surajkumar Harikumar (EE11B075)

function [eps]=proto_thresh_bec_brute(A)
    step=0.01;
    Niter=1000;
    count=0;

    for eps=0:step:1
        [x,xmat,status,complete]=proto_de_iter(A,eps,Niter);
        if status==0
            break
        end
    end
    while count<10
        step=step/2;
        if status ~= 0
            eps = eps+step;
        else
            eps = eps-step;
        end
        [x,xmat,status,complete]=proto_de_iter(A,eps,Niter);
        count=count+1;
    end    
    if status == 1
        eps=eps+step;
    end
end