A=[2,3];
eps=0.2;
[m,n]=size(A);

x=zeros(1,prod(size(A)));
y=zeros(1,prod(size(A)));
x(:)=eps;
x1=zeros(1,sum(length(A)));

Niter=10;
for k=1:Niter
    for i=1:m
        x1=x((i-1)*n+1:(i)*n);
        x2=(1-x1).^A(i,:);  
        y((i-1)*n+1:(i)*n)=1-(prod(x2)./(1-x1));
    end

    for j=1:n
        y1=y(j:n:end);
        y2=y1.^A(:,j);
        x(j:n:end)=eps*(prod(y2))./y1;
    end
end