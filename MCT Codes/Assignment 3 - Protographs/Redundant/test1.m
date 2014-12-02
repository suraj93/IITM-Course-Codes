clear;clc;
A=[2,3;4,2];

step=0.01;
Niter=5000;
count=0;

for eps=0:2*step:1
    [x,xmat,status,complete]=proto_de_iter(A,eps,Niter);
    if status==0
        break
    end
end

while count<10
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
if status == 0
    eps=eps-step;
end
xmat=xmat(1:complete,:)';
figure;
hold on;
for i=1:size(xmat,1)
    plot(1:complete,xmat(i,:),'b');
    
end
