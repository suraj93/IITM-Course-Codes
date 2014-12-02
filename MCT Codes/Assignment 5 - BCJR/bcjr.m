% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Implementing the BCJR decoder for Convolutional Codes
%               over the AWGN channel
%
% Author      : Surajkumar Harikumar (EE11B075)
clear;clc;

k=7;
R=0.5;
N=k/R;
mem=2;
Nstates=2^mem;

% Generator Matrix Convention - [ 1 ; D+D^2 ] -> [1,0,0;0,1,1]
G=[0,1,0;1,1,1];

% Generating the state-output relations for 0-input
% Col 1- Current State; Col2 - Next State; Col 3 - Input
trellis_0=zeros(Nstates,5);
trellis_0(:,1)=0:Nstates-1;
trellis_0(:,2)=floor((0:Nstates-1)/2);
trellis_0(:,3)=zeros(1,Nstates);

Gf=fliplr(G);

%     Output bits
x=bitand(trellis_0(:,1)',bi2de(Gf(1,:)))';
trellis_0(:,4)=mod(sum(de2bi(x)'),2);
x=bitand(trellis_0(:,1)',bi2de(Gf(2,:)))';
trellis_0(:,5)=mod(sum(de2bi(x)'),2);

% Generating the state-output relations for 1-input
% Col 1- Current State; Col2 - Next State; Col 3 - Input
trellis_1=zeros(Nstates,5);
trellis_1(:,1)=0:Nstates-1; 
trellis_1(:,2)=2+floor((0:Nstates-1)/2);
trellis_1(:,3)=ones(1,Nstates);

%     Output Bits
x=bitand(Nstates+trellis_1(:,1)',bi2de(Gf(1,:)))';
trellis_1(:,4)=mod(sum(de2bi(x)'),2);
x=bitand(Nstates+trellis_1(:,1)',bi2de(Gf(2,:)))';
trellis_1(:,5)=mod(sum(de2bi(x)'),2);
    
% trellis_0 =[0,0,0,0,0;1,1,0,0,1];    
% trellis_1=[0,1,1,1,1;1,0,1,1,0];

trellis = [ trellis_0;trellis_1];

prev_state_look=zeros(Nstates,2);
prev_state=zeros(Nstates,2);
for i=1:Nstates
    temp0=find(trellis(:,2)==i-1);
    prev_state_look(i,:)=temp0;
    prev_state(i,:)=trellis(temp0,1);
    
end

input = randi([0,1],k,1)';
input = [ input zeros(1,mem) ]; % Zero padding to return to the zero state

% Using the trellis to encode the message
current_state=0;
enc_input = zeros(1,2*(k+mem));
for i=1:k+mem
    if input(i)==0
        enc_input(2*i-1:2*i)=[ trellis_0(current_state+1,4) trellis_0(current_state+1,5) ];
        current_state=trellis_0(current_state+1,2);
    else
        enc_input(2*i-1:2*i)=[ trellis_1(current_state+1,4) trellis_1(current_state+1,5) ];
        current_state=trellis_1(current_state+1,2);
    end
end

Eb_list=1:4;
for g=1:length(Eb_list)
    R2=k/(2*(k+mem));

    Eb_n0=Eb_list(g);
    Eb_n0
    
    variance=10^(-Eb_n0/10);
    unc(g) = qfunc(0.5/sqrt(variance));

    Es_n0 = Eb_n0*R2;

    La=0;
    Lc=4*Es_n0;


    % BPSK Modulation and Noise adding
    base_sum=0.0;
    Num=5000+2000*Eb_n0;
    for sp=1:Num
        channel_inp = -2*enc_input+1;
        rec=addAWGN(channel_inp,Eb_n0);

        % Gamma - Rows - stage (iteration). Column - State 0,1,2,3...
        gamma_0=zeros(k+mem,Nstates);
        gamma_1=zeros(k+mem,Nstates);
        for i=1:k
            for j=1:Nstates
                gamma_0(i,j)=-0.5*La*1 + 0.5*(rec(2*i-1)*(-2*trellis_0(j,4)+1)+rec(2*i)*(-2*trellis_0(j,5)+1));
                gamma_1(i,j)=0.5*La*1 + 0.5*(rec(2*i-1)*(-2*trellis_1(j,4)+1)+rec(2*i)*(-2*trellis_1(j,5)+1));
            end
        end
        for i=k+1:k+mem
            for j=1:Nstates
                gamma_0(i,j)=0.5*(rec(2*i-1)*(-2*trellis_0(j,4)+1)+rec(2*i)*(-2*trellis_0(j,5)+1));
                gamma_1(i,j)=0.5*(rec(2*i-1)*(-2*trellis_1(j,4)+1)+rec(2*i)*(-2*trellis_1(j,5)+1));
            end
        end

        gamma=[gamma_0';gamma_1'];

        alpha=zeros(Nstates,k+mem);
        alpha(2:Nstates,1)=-1*Inf(1,Nstates-1);

        for i=2:k+mem-1
            for j=1:Nstates
                kk=prev_state_look(j,:);
                l=prev_state(j,:)+1;
                a1=gamma(kk(1),i-1)+alpha(l(1),i-1);
                a2=gamma(kk(2),i-1)+alpha(l(2),i-1);
                if a1==-Inf && a2==-Inf
                    alpha(j,i)=-Inf;
                else
                    b1=max(a1,a2)+log(1+exp(-abs(a1-a2)));
                    alpha(j,i) = b1;
                end
            end
        end

        beta=zeros(Nstates,k+mem);
        beta(2:Nstates,k+mem)=-1*Inf(1,Nstates-1);
        for i=k+mem-1:-1:1
            for j=1:Nstates
                l=[trellis_0(j,2),trellis_1(j,2)]+1;
                kk=[j,j+Nstates];
                a1=gamma(kk(1),i+1)+beta(l(1),i+1);
                a2=gamma(kk(2),i+1)+beta(l(2),i+1);
                if a1==-Inf && a2==-Inf
                    beta(j,i)=-Inf;
                else
                b1=max(a1,a2)+log(1+exp(-abs(a1-a2)));
                beta(j,i) = b1;
                end
            end
        end

        x1=zeros(1,Nstates);
        x2=zeros(1,Nstates);
        L=zeros(1,k+mem);

        for i=1:k
            s0=0;
            s1=0;
            j=1;
            prev0=trellis_0(j,1)+1;
            next0=trellis_0(j,2)+1;
            t0=gamma(prev0,i)+alpha(prev0,i)+beta(next0,i);
            s0=t0;
            prev1=trellis_1(j,1)+1;
            next1=trellis_1(j,2)+1;
            t1=gamma(prev1+Nstates,i)+alpha(prev1,i)+beta(next1,i);
            s1=t1;
            for j=2:Nstates
                prev0=trellis_0(j,1)+1;
                next0=trellis_0(j,2)+1;
                t0=gamma(prev0,i)+alpha(prev0,i)+beta(next0,i);
                x1(j)=t0;
                s0=max(s0,t0)+log(1+exp(-abs(s0-t0)));

                prev1=trellis_1(j,1)+1;
                next1=trellis_1(j,2)+1;
                t1=gamma(prev1+Nstates,i)+alpha(prev1,i)+beta(next1,i);
                x2(j)=t1;
                s1=max(s1,t1)+log(1+exp(-abs(s1-t1)));

            end
            L(i)=s0-s1;
        end

        decoded=zeros(1,k+mem);
        decoded(L<0)=1;

        input;
        decoded;
        base_sum=base_sum+(sum(input~=decoded)~=0);
    end
    err(g)=base_sum/Num;
    err
end

semilogy(Eb_list,err,'.-');
hold on;
semilogy(Eb_list,unc,'r.-');
xlabel('SNR');
xlabel('Block Error Rate');
legend('BCJR decoder','Uncoded Transmission');