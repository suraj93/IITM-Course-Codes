% Course      : Assignment EE5161 Modern Coding Theory
% 
% Description : Belief Propogation Decoder for an LDPC code, with BER-SNR plot     
%
% Data Source : http://www.mathworks.com/matlabcentral/fileexchange/8977-ldpc-code-simulation
%
% Author      : Surajkumar Harikumar (EE11B075)

clear;clc;

H=[1 0 0 1 0 1 ; ...
   0 1 0 1 1 0 ; ...
   0 0 1 0 1 1 ]; 

load 128x256regular

[m,n]=size(H);

m_v2c=zeros(m,n);
m_c2v=zeros(m,n);

SNR=10; %dB
variance=10^(-SNR/10);

Niter=1000;

codeword=ones(1,n);
rec=awgn(codeword,SNR);

%rec=[0.1634,1.5531,2.4584,0.1449,0.0079,0.9883];
init_llr=(2/variance)*rec;

for j=1:m
    listc{j}=find(H(j,:)==0);
end
for i=1:n
    listv{i}=find(H(:,i)==0);
end

SNR_list=2:10;

for l=1:length(SNR_list)
    SNR_l=SNR_list(l);
    variance=10^(-SNR_l/10);
    rec=addAWGN(codeword,variance);
    variance=10^(-SNR_l/10);
    unc(l) = qfunc(0.5/sqrt(variance));

    %rec=[0.1634,1.5531,2.4584,0.1449,0.0079,0.9883];
    init_llr=(2/variance)*rec;

    for j=1:m
        m_v2c(j,:)=init_llr.*H(j,:);
    end

    can=2*atan(1);

    for k=2:10

        for j=1:m
            modc=(m_v2c(j,:));
            modc(listc{j})=can; % This makes the tan() term 1, so effectively, j-i pairs which are not connected have no contribution.
            x1=prod(tan(modc/2))./(tan(modc/2));
            x1(listc{j})=0;
            m_c2v(j,:)=2*atan(x1);
        end

        for i=1:n
            modv=m_c2v(:,i);
            x2=init_llr(i)+sum(modv)-modv;
            x2(listv{i})=0;
            m_v2c(:,i)=x2;
        end
    end

    for i=1:n
        llr_final(i)=init_llr(i)+ sum(m_c2v(:,i));
    end

    dec=sign(llr_final);
    
    actual=sign(rec);
    
    err(l)=sum(dec~=actual)/256;
end

semilogy(SNR_list,err,'.-');
xlabel('SNR (dB)');
ylabel('BER');
hold on;
semilogy(SNR_list,unc,'r.-');
legend('BP decoder','Uncoded Transmission');
