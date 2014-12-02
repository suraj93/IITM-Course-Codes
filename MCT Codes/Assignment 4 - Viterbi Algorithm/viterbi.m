% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Implementing the Viterbi decoder for Convolutional Codes
%               over the AWGN channel
%
% Author      : Surajkumar Harikumar (EE11B075)

clear;clc;

k=10000;
R=0.5;
N=k/R;
mem=2;
Nstates=2^mem;

%Generator Matrix Convention - [ 1 ; D+D^2 ] -> [1,0,0;0,1,1]
G=[0,1,0;1,1,1];

% Generating the state-output relations for 0-input
% Col 1- Current State; Col2 - Next State; Col 3 - Input
    trellis_0=zeros(Nstates,5);
    trellis_0(:,1)=0:Nstates-1;
    trellis_0(:,2)=floor((0:Nstates-1)/2);
    trellis_0(:,3)=zeros(1,Nstates);

    Gf=fliplr(G);

    % Output bits
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

    %Output Bits
    x=bitand(Nstates+trellis_1(:,1)',bi2de(Gf(1,:)))';
    trellis_1(:,4)=mod(sum(de2bi(x)'),2);
    x=bitand(Nstates+trellis_1(:,1)',bi2de(Gf(2,:)))';
    trellis_1(:,5)=mod(sum(de2bi(x)'),2);

trellis = [ trellis_0;trellis_1];


% Message
%input = randi([0,1],k,1)';
%input = [ input zeros(1,mem) ]; % Zero padding to return to the zero state
input = zeros(1,k+mem);

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

Eb_list=1:8
for g=1:length(Eb_list)
    Eb_n0=Eb_list(g);
    
    variance=10^(-Eb_n0/10);
    unc(g) = qfunc(0.5/sqrt(variance));

    % BPSK Modulation and Noise adding
    channel_inp = -2*enc_input+1;
    %rec=awgn(channel_inp,Eb_n0,'measured');
    rec=addAWGN(channel_inp,Eb_n0);
    
    SM = Inf(1,Nstates);
    SM(1)=0;
    msg=[];
    for i = 1:k+mem
        SM_next = Inf(1,Nstates);
        msg_array=zeros(Nstates,1);
        for j=1:Nstates
            BM0=-1*rec(2*i-1)*(-2*trellis_0(j,4)+1)+ -1*rec(2*i)*(-2*trellis_0(j,5)+1);
            BM1=-1*rec(2*i-1)*(-2*trellis_1(j,4)+1)+ -1*rec(2*i)*(-2*trellis_1(j,5)+1);
            if(SM(j)+BM0< SM_next(trellis_0(j,2)+1))
                SM_next(trellis_0(j,2)+1)= SM(j)+BM0;
                msg_array(trellis_0(j,2)+1)=0;
            end
            if(SM(j)+BM1< SM_next(trellis_1(j,2)+1))
                SM_next(trellis_1(j,2)+1)=SM(j)+BM1;
                msg_array(trellis_1(j,2)+1)=1;
            end    
        end
        SM = SM_next;
        a=find(SM==min(SM));
        msg= [msg msg_array(a(1))];
    end
    %input
    %msg
    err(g)=sum(input~=msg)/k
end
semilogy(Eb_list,err,'.-');
hold on;
semilogy(Eb_list,unc,'r.-');
xlabel('SNR');
xlabel('Bit Error Rate');
legend('Viterbi Decoder decoder','Uncoded Transmission');



