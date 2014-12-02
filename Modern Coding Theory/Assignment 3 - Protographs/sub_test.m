% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Script to find the BEC threshold of a protograph, given the
%               parity check matrix. Also plots the density evolution just 
%               below the threshold.
%
% Author      : Surajkumar Harikumar (EE11B075)


clear;clc;
A=[6,1,1;1,4,2];
[M,N]=size(A);
Niter=1000;

eps=proto_thresh_bec_brute(A)
[x,xmat,status,complete]=proto_de_iter(A,eps-0.0001,Niter);

xmat=xmat(1:complete,:)';
figure;
hold on;
for i=1:size(xmat,1)
    j=i-1;
    a1=floor(j/N)+1;
    a2=mod(j,N)+1;
    if A(a1,a2) ~=0
        p3=plot(1:complete,xmat(i,:),'b');
    end
end
xlabel('Iteration Number');
ylabel('Edge Error Probability');
