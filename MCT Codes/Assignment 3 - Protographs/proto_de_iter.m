% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Function to implement density evolution for a protograph,
%               given the base parity check matrix
%
% Author      : Surajkumar Harikumar (EE11B075)

function  [x,xmat,status,conv] = proto_de_iter(A,eps,Niter)

    [m,n]=size(A);
    xmat=zeros(Niter,m*n);
    x=zeros(1,m*n);
    y=zeros(1,m*n);
    x(:)=eps;
    xmat(1,:)=x;
    for k=2:Niter
        x_old=x;
        for i=1:m
            x1=x((i-1)*n+1:(i)*n);
            x2=(1-x1).^A(i,:);  
            y((i-1)*n+1:(i)*n)=1-(prod(x2)./(1-x1));
        end

        for j=1:n
            y1=y(j:n:end);
            y2=y1.^(A(:,j)');
            x(j:n:end)=eps*(prod(y2))./y1;
        end
        xmat(k,:)=x;
        if isempty(find(x>10^-9))
            conv=k;
            status=1;
            return;
        end
        if isempty(find(x_old-x>10^-9))
            conv=k;
            status=0;
            return;
        end
    end
    status=0;
    conv=Niter;
end